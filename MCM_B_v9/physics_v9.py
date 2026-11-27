"""Two-body apex--Moon mission catalogue with separate orbital/surface stages.

The geometry is circular, coplanar, impulsive and zero-SOI.  It is a model
interface, not a real lunar ephemeris, flight readiness claim or certification.
"""
from pathlib import Path
import csv
import json
import math
from scipy.integrate import quad, solve_ivp
from reference import physics_v8 as reference

ROOT = Path(__file__).resolve().parent
DAY = reference.DAY
MU_E, MU_M = reference.MU_E, reference.MU_M
R_E, R_M = reference.R_E, reference.R_M
MOON_DISTANCE = reference.MOON_DISTANCE
SIDEREAL_DAY_S, OMEGA, G0_KM_S2 = reference.SIDEREAL_DAY_S, reference.OMEGA, reference.G0_KM_S2


def _positive(**kw):
    if any(not math.isfinite(float(v)) or v <= 0 for v in kw.values()):
        raise ValueError('Positive finite inputs required: '+', '.join(kw))


def transfer_geometry(initial_tangent_speed_km_s=None, apex_height_km=100000., parking_height_km=100.):
    """Outgoing conic starting tangentially at apex, ending at lunar radius.

    The lower speed is the half-ellipse threshold. The upper speed is free
    corotation release; both endpoints and intermediate conics are admissible
    in this restricted family. Inbound uses its time-reversed radial branch
    while retaining prograde angular momentum.
    """
    base = reference.transfer_geometry(apex_height_km, parking_height_km)
    r0 = base['apex_radius_km']; R = MOON_DISTANCE
    umin = base['earth_ellipse_perigee_speed_km_s']; umax = base['apex_corotation_speed_km_s']
    u = umax if initial_tangent_speed_km_s is None else float(initial_tangent_speed_km_s)
    if not math.isfinite(u) or not umin-1e-12 <= u <= umax+1e-12:
        raise ValueError('Launch speed outside declared tangential family')
    u = max(umin, min(umax, u))
    h = r0*u; energy = .5*u*u-MU_E/r0
    semilatus = h*h/MU_E; eccentricity = semilatus/r0-1
    cosf = (semilatus/R-1)/eccentricity
    if not -1-1e-10 <= cosf <= 1+1e-10:
        raise ValueError('Conic does not reach lunar radius')
    f = math.acos(max(-1., min(1., cosf)))
    vt = h/R
    vr2 = 2*(energy+MU_E/R)-vt*vt
    if vr2 < -1e-10: raise ValueError('Negative lunar-radius radial speed')
    vr = math.sqrt(max(0., vr2))
    vinf = math.hypot(vr, vt-base['moon_circular_speed_km_s'])
    rp = R_M+parking_height_km
    lunar_capture = math.sqrt(vinf*vinf+2*MU_M/rp)-math.sqrt(MU_M/rp)
    coast = quad(lambda z: (semilatus/(1+eccentricity*math.cos(z)))**2/h,
                 0., f, epsabs=1e-6, epsrel=2e-12)[0]/DAY
    base.update(initial_tangent_speed_km_s=u, geocentric_specific_energy_km2_s2=energy,
        geocentric_specific_angular_momentum_km2_s=h, conic_eccentricity=eccentricity,
        conic_semilatus_km=semilatus, geocentric_transfer_angle_rad=f,
        geocentric_transfer_angle_deg=math.degrees(f), earth_transfer_days=coast,
        lunar_radius_radial_speed_km_s=vr, lunar_radius_tangent_speed_km_s=vt,
        moon_relative_v_infinity_km_s=vinf,
        apex_switch_impulse_km_s=abs(umax-u), lunar_capture_impulse_km_s=lunar_capture,
        tug_delta_v_each_way_km_s=abs(umax-u)+lunar_capture,
        return_apex_tangent_speed_before_matching_km_s=u,
        return_apex_matching_impulse_km_s=abs(umax-u),
        original_half_ellipse_reference_days=base['earth_half_ellipse_days'],
        scope='Circular coplanar impulsive zero-SOI conics, variable tangential apex release. No 3D plane transition, finite-SOI or finite-thrust design.')
    return base


def staged_record(transfer='free_release', Isp_tug_s=900., Isp_lander_s=450.,
                  dry_tug_to_net_cargo=.2, dry_lander_to_net_cargo=.2,
                  surface_loss_margin_km_s=.3, min_structural_fraction=.05,
                  initial_tangent_speed_km_s=None):
    _positive(Isp_tug_s=Isp_tug_s, Isp_lander_s=Isp_lander_s,
              dry_tug_to_net_cargo=dry_tug_to_net_cargo,
              dry_lander_to_net_cargo=dry_lander_to_net_cargo)
    if not math.isfinite(surface_loss_margin_km_s) or surface_loss_margin_km_s < 0:
        raise ValueError('Nonnegative finite surface impulse margin required')
    if not math.isfinite(min_structural_fraction) or not 0 < min_structural_fraction < 1:
        raise ValueError('Structural scenario screen must be in (0,1)')
    if transfer not in ['free_release','half_ellipse','tangential_grid']:
        raise ValueError('Unknown transfer architecture')
    if transfer == 'half_ellipse':
        initial_tangent_speed_km_s = reference.transfer_geometry()['earth_ellipse_perigee_speed_km_s']
    elif transfer == 'free_release':
        initial_tangent_speed_km_s = None
    elif initial_tangent_speed_km_s is None:
        raise ValueError('Grid transfer requires a launch speed')
    geo = transfer_geometry(initial_tangent_speed_km_s)
    dT,dL = dry_tug_to_net_cargo,dry_lander_to_net_cargo
    dvT = geo['tug_delta_v_each_way_km_s']
    dvL = geo['lunar_ideal_descent_or_ascent_km_s']+surface_loss_margin_km_s
    AT = math.exp(dvT/(G0_KM_S2*Isp_tug_s)); BT = AT
    AL = math.exp(dvL/(G0_KM_S2*Isp_lander_s)); BL = AL
    ML = AL*(1+dL*BL)
    PTr = (dT+dL)*(BT-1)
    beta = AT*(ML+dT+PTr)
    touchdown = 1+dL*BL
    PLr = dL*(BL-1)
    tug_prop = beta-ML-dT
    lander_prop = ML-1-dL
    epsT = dT/(dT+tug_prop); epsL = dL/(dL+lander_prop)
    coast = geo['earth_transfer_days']+geo['lunar_half_ellipse_days']
    phase = geo['single_apex_phase_cycle_days']
    encounter, surface, apex, separation, dock = 2.,3.,7.,.5,.5
    ready = coast+phase+encounter+separation
    cycle = 2*coast+2*phase+2*encounter+surface+apex+separation+dock
    # A receiving delay is appended after the outbound portion. Independently
    # rounded upper bounds cannot be subtracted to obtain its remaining tail:
    # ceil(cycle)-ceil(ready) can be SMALLER than cycle-ready. Bound the tail
    # directly, then concatenate the two integer contracts. Keeping the legacy
    # cycle field equal to their sum also makes old cycle-minus-ready consumers
    # safe, although it is one day looser than ceil(raw cycle) in some records.
    tail = coast+phase+encounter+surface+apex+dock
    ready_integer = math.ceil(ready)
    tail_integer = math.ceil(tail)
    outward_consumed = beta-(ML+dT+PTr)+ML-touchdown
    nominal = Isp_tug_s==900 and Isp_lander_s==450 and dT==.2 and dL==.2 and surface_loss_margin_km_s==.3
    return dict(name=f'{transfer}_tug{Isp_tug_s:g}_lander{Isp_lander_s:g}_dT{dT:.2f}_dL{dL:.2f}_margin{surface_loss_margin_km_s:.2f}'+(f'_u{geo["initial_tangent_speed_km_s"]:.9f}' if transfer=='tangential_grid' else ''),
        architecture='orbital_tug_chemical_lander', transfer_mode=transfer,
        geometry=geo, Isp_tug_s=Isp_tug_s,Isp_lander_s=Isp_lander_s,
        dry_tug_to_net_cargo_ratio=dT,dry_lander_to_net_cargo_ratio=dL,
        surface_loss_margin_each_way_km_s=surface_loss_margin_km_s,
        tug_delta_v_each_way_km_s=dvT,lander_delta_v_each_way_km_s=dvL,
        beta_outbound_per_net_cargo=beta,return_dry_per_net_cargo=dT+dL,
        landing_mass_per_net_cargo=touchdown,
        recurring_apex_resupply_mass_per_net_cargo=beta-dT-dL,
        initial_dry_hardware_per_net_cargo=dT+dL,
        initial_lander_mass_at_lunar_orbit_per_net_cargo=ML,
        tug_mass_parked_in_lunar_orbit_per_net_cargo=dT+PTr,
        tug_return_wet_mass_after_rendezvous_per_net_cargo=(dT+dL)*BT,
        return_tug_propellant_per_net_cargo=PTr, return_lander_propellant_per_net_cargo=PLr,
        return_propellant_carried_per_net_cargo=PTr+PLr,
        tug_propellant_total_per_net_cargo=tug_prop,
        lander_propellant_total_per_net_cargo=lander_prop,
        outbound_propellant_per_net_cargo=outward_consumed,
        tug_structural_dry_fraction=epsT,lander_structural_dry_fraction=epsL,
        structural_dry_fraction=min(epsT,epsL),
        min_structural_fraction=min_structural_fraction,
        structural_screen_pass=min(epsT,epsL)>=min_structural_fraction,
        structural_screen_is_scenario=True,structural_feasibility_verified=False,
        structural_fraction_denominator='Each component dry/(component dry+own total propellant); excludes carried payload.',
        outbound_flight_days=coast,outbound_phase_wait_bound_days=phase,
        return_phase_wait_bound_days=phase,
        outbound_ready_to_touchdown_days_scenario=ready,
        outbound_ready_to_touchdown_days_integer_scenario=ready_integer,
        return_tail_unrounded_days_scenario=tail,
        return_tail_upper_days=tail_integer,
        return_cycle_unrounded_days_scenario=cycle,
        return_cycle_direct_ceiling_days=math.ceil(cycle),
        return_cycle_days=ready_integer+tail_integer,
        integer_cycle_scope='Sum of separately bounded outbound-ready and post-touchdown-return tail; never subtract two independent ceilings to derive a tail.',
        encounter_time_allowance_per_leg_days_scenario=encounter,
        surface_service_days_scenario=surface,apex_service_days_scenario=apex,
        lunar_orbit_separation_days_scenario=separation,
        return_rendezvous_dock_days_scenario=dock,
        max_departures_per_phase_window_scenario=2,
        vehicle_return_required=True, new_vehicle_required_per_delivery=False,
        recommended_for_conditional_study=transfer=='free_release' and nominal and min(epsT,epsL)>=min_structural_fraction,
        net_cargo_mass_scope='Delivered payload includes packaging. Usable water fraction is separate.',
        recurring_lift_scope='All return propellant leaves apex initially. Returned dry structures lifted only once; no lunar refuelling.',
        time_scope='Declared operations and phase-wait budget before additional receiving queue. Not a calibrated real-world flight-time guarantee.',
        scope='Finite conceptual mission catalogue. No real 3D, finite-SOI, finite-thrust, structural, cryogenic, nuclear-safety or capture-tolerance certification; not a global trajectory optimum.')


def mission_catalog():
    g = reference.transfer_geometry()
    lo,hi = g['earth_ellipse_perigee_speed_km_s'],g['apex_corotation_speed_km_s']
    records = []
    for i in range(21):
        if i==0: rec=staged_record('half_ellipse')
        elif i==20: rec=staged_record('free_release')
        else: rec=staged_record('tangential_grid',initial_tangent_speed_km_s=lo+(hi-lo)*i/20)
        rec['study_group']='nominal_21_speed_grid';records.append(rec)
    for I,chi,margin in [(850.,.2,.3),(950.,.2,.3),(900.,.15,.3),(900.,.25,.3),(900.,.2,.1),(900.,.2,.5)]:
        rec=staged_record('free_release',Isp_tug_s=I,dry_tug_to_net_cargo=chi,
                           dry_lander_to_net_cargo=chi,surface_loss_margin_km_s=margin)
        rec['study_group']='one_factor_engineering_scenario';records.append(rec)
    return records


def chosen_mission():
    return next(x for x in mission_catalog() if x['recommended_for_conditional_study'])


def _phase_wait(request_day,phase0,rate):
    """Smallest nonnegative wait until phase0+rate*t==0 modulo2pi."""
    phi=(phase0+rate*request_day*DAY)%(2*math.pi)
    return ((2*math.pi-phi)%(2*math.pi))/rate/DAY


def validation(records=None):
    records=records or mission_catalog();max_mass_error=0.;max_pos=0.;max_vel=0.;max_energy=0.
    phase_checked=0;max_phase_residual=0.;max_phase_wait=0.
    for rec in records:
        g=rec['geometry'];dT=rec['dry_tug_to_net_cargo_ratio'];dL=rec['dry_lander_to_net_cargo_ratio']
        AT=math.exp(rec['tug_delta_v_each_way_km_s']/(G0_KM_S2*rec['Isp_tug_s']))
        AL=math.exp(rec['lander_delta_v_each_way_km_s']/(G0_KM_S2*rec['Isp_lander_s']))
        beta=rec['beta_outbound_per_net_cargo'];ML=rec['initial_lander_mass_at_lunar_orbit_per_net_cargo']
        PTr=rec['return_tug_propellant_per_net_cargo']
        # Sequential burn reconstruction follows the physical staging timeline.
        states=[beta/AT-(ML+dT+PTr),ML/AL-rec['landing_mass_per_net_cargo'],
                (ML/AL-1)/AL-dL,(dT+PTr+dL)/AT-(dT+dL),
                beta-rec['outbound_propellant_per_net_cargo']-1-PTr-rec['return_lander_propellant_per_net_cargo']-(dT+dL)]
        max_mass_error=max(max_mass_error,max(map(abs,states)))
        assert math.isclose(rec['return_tail_unrounded_days_scenario'],
                            rec['return_cycle_unrounded_days_scenario']-rec['outbound_ready_to_touchdown_days_scenario'],
                            rel_tol=1e-13, abs_tol=1e-13)
        assert rec['return_tail_upper_days']>=rec['return_tail_unrounded_days_scenario']
        assert rec['outbound_ready_to_touchdown_days_integer_scenario']>=rec['outbound_ready_to_touchdown_days_scenario']
        assert rec['return_cycle_days']==rec['outbound_ready_to_touchdown_days_integer_scenario']+rec['return_tail_upper_days']
        r0=g['apex_radius_km'];u=g['initial_tangent_speed_km_s'];f=g['geocentric_transfer_angle_rad'];tf=g['earth_transfer_days']*DAY
        def rhs(t,z):
            r=math.hypot(z[0],z[1]);return [z[2],z[3],-MU_E*z[0]/r**3,-MU_E*z[1]/r**3]
        z=solve_ivp(rhs,[0,tf],[r0,0.,0.,u],method='DOP853',rtol=1e-12,atol=1e-12)
        assert z.success
        target=(MOON_DISTANCE*math.cos(f),MOON_DISTANCE*math.sin(f))
        pos=math.hypot(z.y[0,-1]-target[0],z.y[1,-1]-target[1]);max_pos=max(max_pos,pos)
        # Return radial branch starts at true anomaly -f and arrives at perigee.
        vr=g['lunar_radius_radial_speed_km_s'];vt=g['lunar_radius_tangent_speed_km_s']
        er=(math.cos(f),-math.sin(f));et=(math.sin(f),math.cos(f))
        initial=[MOON_DISTANCE*er[0],MOON_DISTANCE*er[1],-vr*er[0]+vt*et[0],-vr*er[1]+vt*et[1]]
        ret=solve_ivp(rhs,[0,tf],initial,method='DOP853',rtol=1e-12,atol=1e-12)
        assert ret.success
        retpos=math.hypot(ret.y[0,-1]-r0,ret.y[1,-1]);retvel=math.hypot(ret.y[2,-1],ret.y[3,-1]-u)
        max_pos=max(max_pos,retpos);max_vel=max(max_vel,retvel)
        radii=(z.y[0]**2+z.y[1]**2)**.5
        energy=.5*(z.y[2]**2+z.y[3]**2)-MU_E/radii
        max_energy=max(max_energy,max(abs(energy-g['geocentric_specific_energy_km2_s2'])))
        n=math.sqrt((MU_E+MU_M)/MOON_DISTANCE**3);rate=OMEGA-n
        # Arbitrary initial longitudes; model intercept condition is tested
        # separately for outgoing and inbound branches, not merely one period.
        for i in range(33):
            req=3650*i/32;thetaA=.213;thetaM=1.347
            tau=g['earth_transfer_days']*DAY
            outphase=thetaA-thetaM+f-n*tau
            outwait=_phase_wait(req,outphase,rate)
            t=(req+outwait)*DAY
            residual=math.remainder(thetaA+OMEGA*t+f-(thetaM+n*(t+tau)),2*math.pi)
            retphase=thetaA-thetaM+OMEGA*tau-f
            retwait=_phase_wait(req,retphase,rate)
            tr=(req+retwait)*DAY
            retres=math.remainder(thetaA+OMEGA*(tr+tau)-(thetaM+n*tr+f),2*math.pi)
            phase_checked+=2;max_phase_residual=max(max_phase_residual,abs(residual),abs(retres))
            max_phase_wait=max(max_phase_wait,outwait,retwait)
            assert outwait<=rec['outbound_phase_wait_bound_days']+1e-10
            assert retwait<=rec['return_phase_wait_bound_days']+1e-10
    assert max_mass_error<1e-10 and max_pos<1e-3 and max_vel<1e-7 and max_energy<1e-9
    assert max_phase_residual<1e-8
    nominal=[x for x in records if x['study_group']=='nominal_21_speed_grid']
    assert min(nominal,key=lambda z:z['beta_outbound_per_net_cargo'])['transfer_mode']=='free_release'
    assert len([x for x in records if x['recommended_for_conditional_study']])==1
    invalid=0
    for kw in [dict(Isp_tug_s=0),dict(Isp_lander_s=-1),dict(dry_tug_to_net_cargo=0),dict(dry_lander_to_net_cargo=math.inf),dict(surface_loss_margin_km_s=-1),dict(min_structural_fraction=1),dict(transfer='invalid')]:
        try:staged_record(**kw)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid input accepted')
    return dict(mission_mass_chains=len(records),max_mass_reconstruction_error=max_mass_error,
        outgoing_and_incoming_ODE_integrations=2*len(records),
        max_ODE_endpoint_position_error_km=max_pos,max_return_velocity_error_km_s=max_vel,
        max_ODE_specific_energy_error_km2_s2=max_energy,
        circular_interception_phase_cases=phase_checked,max_phase_equation_residual_rad=max_phase_residual,
        max_observed_phase_wait_days=max_phase_wait,invalid_inputs_rejected=invalid,
        nominal_speed_grid_free_release_has_lowest_beta=True,
        separately_bounded_outbound_and_return_tail_checked=len(records),
        scope='Independent arithmetic, ODE and circular-phase checks of the stated idealized model. No real ephemeris/window/finite-SOI validation.')


def run():
    records=mission_catalog();checks=validation(records)
    result=dict(version='v9_physics',chosen_mission=chosen_mission(),missions=records,checks=checks,
        sources=[dict(url='https://ssd.jpl.nasa.gov/astro_par.html',role='JPL DE440 gravitational parameters, day and sidereal-day constants; observed physical constants, not future hardware.'),
            dict(url='https://ntrs.nasa.gov/citations/20190032556',role='NASA2019 conceptual NTP background.900s is a declared performance scenario, not validated hardware for this mission.'),
            dict(url='https://arxiv.org/abs/2008.05244',role='Peet2020 orbital release architecture background. Paper warns of plane-transition/alignment restrictions; v9 lunar conics are project derivations.')],
        truth='Geometry and mass results are conditional calculations. Hardware ratios, margins, operations times and port schedules are named design assumptions.')
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/physics_v9.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    fields=['name','transfer_mode','study_group','beta_outbound_per_net_cargo','tug_delta_v_each_way_km_s','landing_mass_per_net_cargo','outbound_ready_to_touchdown_days_integer_scenario','return_cycle_days','structural_screen_pass']
    with (ROOT/'results/physics_v9_catalogue.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:z[k] for k in fields} for z in records)
    print(json.dumps(dict(version=result['version'],missions=len(records),chosen=chosen_mission()['name'],checks=checks),ensure_ascii=False))
    return result


if __name__=='__main__':run()
