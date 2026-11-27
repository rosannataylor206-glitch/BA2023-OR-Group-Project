"""Independent LP cross-check of the construction share choice.

Scope note
----------
This script is a VERIFICATION TOOL.  The main v9 pipeline does not solve an LP
and must not be described as doing so.  Here we write the share decision as a
small two-variable linear program, solve it with scipy.optimize.linprog, and
compare the optimum with the analytic balancing share already used by
joint_v9.share_catalogue().  Agreement means the closed-form share is the exact
optimum of the declared LP; disagreement would mean the affine certificate
celebrated in the report is not the minimiser of the declared metric.

Model (per operating mode)
--------------------------
Decision variables
    s   elevator share of the 100 Mt construction target, dimensionless, [0,1]
    z   upper bound on construction completion time, days

Objective
    minimise z

Constraints
    z >= aE * s + bE          (elevator-chain completion upper bound, days)
    z >= aR * (1 - s) + bR    (ground-rocket completion upper bound, days)
    0 <= s <= 1

Parameters (all days per unit share, derived from the affine certificate)
    aE = T / (3 * rE),  bE = cE / rE
    aR = T / (10 * rR), bR = cR / rR
    T   generic construction target (t)
    rE  guaranteed elevator rate per harbour (t/day)
    rR  guaranteed rocket rate per site (t/day)
    cE  elevator affine intercept (t), cR rocket affine intercept (t)

Reported evidence
    lp_share, lp_z, analytic_share, share_gap,
    certificate_days_at_lp, certificate_days_at_analytic,
    constraint_residuals, solver status/message.
"""
from pathlib import Path
import json
import math

from scipy.optimize import linprog

from physics_v9 import chosen_mission
from construction_v9 import ConstructionInputs, ideal_inputs, plan_construction

ROOT = Path(__file__).resolve().parent
TARGET_T = 100_000_000.


def affine_coefficients(inputs, mission, target_t=TARGET_T):
    """Return (aE,bE,aR,bR) in days and days/share for one operating mode."""
    e_plan = plan_construction(1., inputs, mission, target_t=target_t)['routes']['E']
    r_plan = plan_construction(0., inputs, mission, target_t=target_t)['routes']['R']
    rE = e_plan['affine_net_rate_t_day_per_source']       # t/day per harbour
    cE = e_plan['affine_intercept_t_per_source']          # t
    rR = r_plan['affine_net_rate_t_day_per_source']       # t/day per site
    cR = r_plan['affine_intercept_t_per_source']          # t
    return dict(
        aE=target_t/(3.*rE), bE=cE/rE,
        aR=target_t/(10.*rR), bR=cR/rR,
        rE_t_day=rE, cE_t=cE, rR_t_day=rR, cR_t=cR)


def solve_share_lp(aE, bE, aR, bR):
    """Solve min z s.t. z>=aE s+bE, z>=aR(1-s)+bR, 0<=s<=1."""
    c = [0., 1.]
    A_ub = [[aE, -1.], [-aR, -1.]]
    b_ub = [-bE, -(aR + bR)]
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0., 1.), (None, None)],
                     method='highs')
    return result


def analytic_share(aE, bE, aR, bR):
    """Crossing point of the two affine bounds, clipped to [0,1]."""
    return max(0., min(1., (aR + bR - bE) / (aE + aR)))


def check_mode(label, inputs, mission):
    coef = affine_coefficients(inputs, mission)
    res = solve_share_lp(coef['aE'], coef['bE'], coef['aR'], coef['bR'])
    if not res.success:
        return dict(mode=label, solved=False, message=res.message)
    s_lp = float(res.x[0]); z_lp = float(res.x[1])
    s_an = analytic_share(coef['aE'], coef['bE'], coef['aR'], coef['bR'])
    e_at_lp = coef['aE']*s_lp + coef['bE']
    r_at_lp = coef['aR']*(1.-s_lp) + coef['bR']
    # Full certificate (not just the affine form) at both shares.
    plan_lp = plan_construction(s_lp, inputs, mission)
    plan_an = plan_construction(s_an, inputs, mission)
    return dict(
        mode=label,
        solved=True,
        parameters=coef,
        lp=dict(share=s_lp, z_days=z_lp,
                status=res.status, message=res.message,
                nit=int(getattr(res, 'nit', 0) or 0)),
        analytic=dict(share=s_an),
        agreement=dict(share_gap_abs=abs(s_lp - s_an),
                       lp_z_days=z_lp,
                       bound_E_at_lp_days=e_at_lp,
                       bound_R_at_lp_days=r_at_lp,
                       residual_E_days=abs(z_lp - e_at_lp),
                       residual_R_days=abs(z_lp - r_at_lp)),
        certificate=dict(
            days_at_lp_share=plan_lp['construction_completion_upper_days'],
            days_at_analytic_share=plan_an['construction_completion_upper_days'],
            years_at_lp_share=plan_lp['construction_completion_upper_years'],
            years_at_analytic_share=plan_an['construction_completion_upper_years'],
            delivered_t_at_lp_share=plan_lp['guaranteed_delivered_t']),
        consistent=(abs(s_lp - s_an) <= 1e-9 and
                    plan_lp['construction_completion_upper_days'] ==
                    plan_an['construction_completion_upper_days']))


def run():
    mission = chosen_mission()
    rows = []
    for label, inputs in [('ideal', ideal_inputs()), ('fault', ConstructionInputs())]:
        rows.append(check_mode(label, inputs, mission))
    out = dict(
        version='v9_share_lp_cross_check',
        target_t=TARGET_T,
        purpose='Independent LP cross-check of the closed-form balancing share; verification only.',
        not_used_by_main_pipeline=True,
        model=dict(
            variables=['s: elevator share of the construction target (dimensionless, [0,1])',
                       'z: construction completion upper bound (days)'],
            objective='minimise z',
            constraints=['z >= aE*s + bE',
                         'z >= aR*(1-s) + bR',
                         '0 <= s <= 1'],
            parameter_units=dict(aE='days per unit share', bE='days',
                                 aR='days per unit share', bR='days',
                                 rE_t_day='guaranteed elevator tonnes per day per harbour',
                                 rR_t_day='guaranteed rocket tonnes per day per site',
                                 cE_t='elevator affine intercept (tonnes)',
                                 cR_t='rocket affine intercept (tonnes)')),
        cases=rows,
        scope=('Finite two-route share decomposition under the declared affine '
               'sufficient certificates. Agreement shows the analytic share is the '
               'LP optimum of this declared metric; it is not evidence that the main '
               'pipeline uses simplex, and it does not certify global optimality.'),
        all_consistent=all(r.get('consistent', False) for r in rows))
    results = ROOT / 'results'
    results.mkdir(exist_ok=True)
    (results / 'share_lp_check_v9.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({r['mode']: {
        'lp_share': round(r['lp']['share'], 8) if r.get('solved') else None,
        'analytic_share': round(r['analytic']['share'], 8) if r.get('solved') else None,
        'consistent': r.get('consistent')} for r in rows}, ensure_ascii=False))
    return out


if __name__ == '__main__':
    run()
