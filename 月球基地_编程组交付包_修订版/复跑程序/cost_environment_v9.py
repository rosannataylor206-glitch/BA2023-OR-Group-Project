"""Parameterized constant-technology spending and an explicit emissions proxy.

The numerical coefficient scenarios are illustrations, not forecasts, current
Moon-delivery prices, confidence intervals, or complete life-cycle assessments.
Historical NASA/EIA/FAA benchmarks are documented separately in evidence.
"""
from copy import deepcopy
import math

HISTORICAL_BENCHMARKS = {
    'NASA_Psyche_2020_contract_USD': 117_000_000.,
    'EIA_2024_US_industrial_electricity_USD_kWh': .0813,
    'EIA_2023_US_generation_CO2_kg_kWh': .81 * .45359237,
    'FAA_2020_Falcon_Heavy_direct_launch_CO2_kg': 11_613. / 10. * 1000.,
}

# Each tuple is (illustration, lower scenario, upper scenario). A box of
# coefficient values is deliberately wide; it is NOT a statistical interval.
# Launch price covers flight-specific vehicle, propellant and launch services;
# standing facility upkeep/renewal is charged separately below.
COST_COEFFICIENTS = {
    'earth_electricity_USD_kWh': (.0813, .04, .20),
    'lift_nonenergy_USD_kg': (100., 20., 500.),
    'E_propellant_procurement_USD_kg': (10., 2., 100.),
    'R_flight_services_USD': (117e6, 58.5e6, 585e6),
    'E_hull_manufacture_USD': (500e6, 100e6, 2e9),
    'E_flight_overhaul_USD': (2e6, .2e6, 20e6),
    'water_module_manufacture_USD': (20e6, 2e6, 200e6),
    'tank_manufacture_USD': (1e6, .1e6, 10e6),
    'lunar_electricity_USD_kWh': (1., .2, 10.),
    'lunar_power_capacity_USD_kW': (20_000., 2_000., 200_000.),
    'warehouse_capacity_USD_t': (10_000., 1_000., 100_000.),
    'receiving_slot_capacity_USD': (200e6, 20e6, 2e9),
    'harbour_annual_upkeep_USD': (1e9, .1e9, 10e9),
    'R_site_annual_upkeep_USD': (50e6, 5e6, 500e6),
    'E_hull_annual_upkeep_USD': (2e6, .2e6, 20e6),
    'warehouse_annual_upkeep_USD_t': (100., 10., 1_000.),
    'receiving_slot_annual_upkeep_USD': (2e6, .2e6, 20e6),
}

ENVIRONMENT_COEFFICIENTS = {
    'earth_grid_CO2_kg_kWh': (HISTORICAL_BENCHMARKS['EIA_2023_US_generation_CO2_kg_kWh'], .02, .8),
    'R_direct_launch_CO2_kg': (HISTORICAL_BENCHMARKS['FAA_2020_Falcon_Heavy_direct_launch_CO2_kg'], 580_650., 3_483_900.),
    'R_upstream_CO2_proxy_kg': (300_000., 100_000., 5_000_000.),
    'E_propellant_production_CO2_proxy_kg_kg': (10., .1, 30.),
    'lunar_energy_upstream_CO2_proxy_kg_kWh': (.1, .001, 10.),
}

_SCENARIO_OVERRIDES = {
    'central': {},
    'rocket_favoured': {'R_flight_services_USD': 58.5e6, 'lift_nonenergy_USD_kg': 500.,
                        'E_hull_manufacture_USD': 2e9, 'E_propellant_procurement_USD_kg': 100.},
    'elevator_favoured': {'R_flight_services_USD': 585e6, 'lift_nonenergy_USD_kg': 20.,
                          'E_hull_manufacture_USD': 100e6, 'E_propellant_procurement_USD_kg': 2.},
    'low_carbon_grid': {'earth_grid_CO2_kg_kWh': .02},
    'high_carbon_grid': {'earth_grid_CO2_kg_kWh': .8},
}

FEATURE_ALIASES = {
    'E_new_lift_t': ['E_new_lift_t', 'E_lift_mass_t', 'fullpacket_lift_mass_t'],
    'E_energy_kWh': ['E_energy_kWh', 'earth_lift_energy_kWh', 'lift_energy_kWh'],
    'E_propellant_t': ['E_propellant_t', 'E_propellant_lift_t'],
    'R_launches': ['R_launches', 'R_flights', 'R_full_attempts'],
    'E_hulls_initial': ['E_hulls_initial', 'E_hulls_manufactured', 'E_hulls_total'],
    'E_flights': ['E_flights', 'E_full_attempts'],
    'water_modules': ['water_modules', 'processing_modules'],
    'tanks': ['tanks', 'tank_compartments'],
    'lunar_energy_kWh': ['lunar_energy_kWh', 'water_plant_energy_kWh'],
    'lunar_power_capacity_kW': ['lunar_power_capacity_kW', 'plant_power_kW'],
    'warehouse_capacity_t': ['warehouse_capacity_t', 'anchor_installed_capacity_t'],
    'lunar_receiving_slots': ['lunar_receiving_slots', 'receiving_slots'],
    'active_harbours': ['active_harbours'],
    'active_R_sites': ['active_R_sites', 'active_rocket_sites'],
    'infrastructure_years': ['infrastructure_years', 'mission_years', 'construction_years'],
    'harbour_service_years': ['harbour_service_years', 'active_harbour_years'],
    'R_site_service_years': ['R_site_service_years', 'active_R_site_years'],
    'hull_service_years': ['hull_service_years'],
    'warehouse_t_years': ['warehouse_t_years'],
    'receiving_slot_years': ['receiving_slot_years'],
}


def _nonnegative(value, name):
    v=float(value)
    if isinstance(value, bool) or not math.isfinite(v) or v < 0:
        raise ValueError(name + ' must be finite and nonnegative')
    return v


def normalize_features(features):
    """Return a unit-explicit vector and disclose derived/missing dimensions.

    An absent dimension is not silently certified as irrelevant: missing input
    keys are returned to the caller. Zero must be supplied explicitly for a
    genuinely unused route. Derived service-years are conservative accounting
    exposures if all purchased capacity is retained for the supplied horizon.
    """
    if not isinstance(features, dict):
        raise TypeError('features must be a dict')
    z = {}; missing = []; derived = []
    for target, aliases in FEATURE_ALIASES.items():
        matches = [a for a in aliases if a in features]
        if matches:
            v = [_nonnegative(features[a], a) for a in matches]
            if max(v)-min(v) > 1e-8*max(1., max(v)):
                raise ValueError('Conflicting aliases for ' + target)
            z[target] = v[0]
        else:
            missing.append(target)
    if 'E_energy_kWh' not in z and 'E_new_lift_t' in z:
        k = _nonnegative(features.get('lift_kWh_kg', 19.215324422302), 'lift_kWh_kg')
        z['E_energy_kWh'] = 1000.*z['E_new_lift_t']*k
        derived.append('E_energy_kWh = 1000 E_new_lift_t lift_kWh_kg')
        missing.remove('E_energy_kWh')
    exposures = {
        'harbour_service_years': ('active_harbours', 'infrastructure_years'),
        'R_site_service_years': ('active_R_sites', 'infrastructure_years'),
        'hull_service_years': ('E_hulls_initial', 'infrastructure_years'),
        'warehouse_t_years': ('warehouse_capacity_t', 'infrastructure_years'),
        'receiving_slot_years': ('lunar_receiving_slots', 'infrastructure_years'),
    }
    for target, (a,b) in exposures.items():
        if target not in z and a in z and b in z:
            z[target] = z[a]*z[b]
            derived.append(target+' = '+a+' '+b)
            missing.remove(target)
    # Missing features remain visible. evaluate_features uses a zero extension
    # solely to evaluate the supplied partial vector and marks it incomplete.
    return dict(vector={k:z.get(k, 0.) for k in FEATURE_ALIASES},
                missing_features=missing, derived_features=derived)


def get_scenario_defs():
    return dict(
        version='v9_parameter_cost_and_environment',
        scenario_identity='Illustrative constant-technology coefficient cases; not future quotations, forecasts or probability intervals.',
        cost_coefficients={k:dict(central=v[0], lower=v[1], upper=v[2]) for k,v in COST_COEFFICIENTS.items()},
        environment_coefficients={k:dict(central=v[0], lower=v[1], upper=v[2]) for k,v in ENVIRONMENT_COEFFICIENTS.items()},
        scenarios=deepcopy(_SCENARIO_OVERRIDES), historical_benchmarks=deepcopy(HISTORICAL_BENCHMARKS),
        time_basis='Undiscounted constant-technology spending exposure. No inflation, financing, learning, technological obsolescence, or present-value interpretation.',
        price_boundary='R_flight_services includes vehicle/propellant/flight-specific launch services, but excludes separately charged standing-facility upkeep. E lift energy, nonenergy handling, propellant purchase, hull manufacturing and overhaul are separate. Annual upkeep is a service-renewal accounting coefficient, not an assertion that one physical asset lasts centuries.',
        incomplete_environment=['Stratospheric soot/black carbon, NOx, water-vapour and ozone chemistry',
                                'Nuclear/radiological impacts of the orbital tug',
                                'Tether and infrastructure material manufacturing, land/ocean ecology, noise, debris and accident consequences'],
        sunk_infrastructure='The task starts after the space-elevator system is built. Historic construction of that pre-existing system is excluded from incremental spending; continued operations/renewal are charged. New hull and water equipment manufacturing is charged. Warehouse and receiving capacity coefficients procure/reserve an exogenous ready service; provider deployment mass/time is outside the physical cargo ledger.',
        budget_identity='All allocated full jobs and equipment are conservatively committed, including potentially unlaunched tail stock. Values rank declared reserved-spending upper budgets, not exact realized expenditure or expected cost.')


def _coefficient_values(scenario):
    known = dict(COST_COEFFICIENTS, **ENVIRONMENT_COEFFICIENTS)
    if isinstance(scenario, str):
        if scenario not in _SCENARIO_OVERRIDES: raise ValueError('Unknown coefficient scenario')
        overrides = _SCENARIO_OVERRIDES[scenario]; name = scenario
    elif isinstance(scenario, dict):
        overrides = scenario; name = 'custom'
    else: raise TypeError('scenario must be a known name or coefficient dict')
    unknown = set(overrides)-set(known)
    if unknown: raise ValueError('Unknown coefficients: '+', '.join(sorted(unknown)))
    vals = {k:v[0] for k,v in known.items()}
    for k,v in overrides.items(): vals[k]=_nonnegative(v,k)
    return name, vals


def _cost_quantities(f):
    return {
        'earth_electricity_USD_kWh': f['E_energy_kWh'],
        'lift_nonenergy_USD_kg': f['E_new_lift_t']*1000.,
        'E_propellant_procurement_USD_kg': f['E_propellant_t']*1000.,
        'R_flight_services_USD': f['R_launches'],
        'E_hull_manufacture_USD': f['E_hulls_initial'],
        'E_flight_overhaul_USD': f['E_flights'],
        'water_module_manufacture_USD': f['water_modules'],
        'tank_manufacture_USD': f['tanks'],
        'lunar_electricity_USD_kWh': f['lunar_energy_kWh'],
        'lunar_power_capacity_USD_kW': f['lunar_power_capacity_kW'],
        'warehouse_capacity_USD_t': f['warehouse_capacity_t'],
        'receiving_slot_capacity_USD': f['lunar_receiving_slots'],
        'harbour_annual_upkeep_USD': f['harbour_service_years'],
        'R_site_annual_upkeep_USD': f['R_site_service_years'],
        'E_hull_annual_upkeep_USD': f['hull_service_years'],
        'warehouse_annual_upkeep_USD_t': f['warehouse_t_years'],
        'receiving_slot_annual_upkeep_USD': f['receiving_slot_years'],
    }


def _environment_quantities(f):
    return {
        'earth_grid_CO2_kg_kWh': f['E_energy_kWh'],
        'R_direct_launch_CO2_kg': f['R_launches'],
        'R_upstream_CO2_proxy_kg': f['R_launches'],
        'E_propellant_production_CO2_proxy_kg_kg': f['E_propellant_t']*1000.,
        'lunar_energy_upstream_CO2_proxy_kg_kWh': f['lunar_energy_kWh'],
    }


def evaluate_features(features, scenario='central'):
    normalized = normalize_features(features); f=normalized['vector']
    name, c = _coefficient_values(scenario)
    cq = _cost_quantities(f); eq = _environment_quantities(f)
    cost_parts = {k:q*c[k] for k,q in cq.items()}
    env_parts = {k:q*c[k] for k,q in eq.items()}
    lower = sum(q*COST_COEFFICIENTS[k][1] for k,q in cq.items())
    upper = sum(q*COST_COEFFICIENTS[k][2] for k,q in cq.items())
    elower = sum(q*ENVIRONMENT_COEFFICIENTS[k][1] for k,q in eq.items())
    eupper = sum(q*ENVIRONMENT_COEFFICIENTS[k][2] for k,q in eq.items())
    outside = [k for k,v in c.items() if not (dict(COST_COEFFICIENTS,**ENVIRONMENT_COEFFICIENTS)[k][1] <= v <= dict(COST_COEFFICIENTS,**ENVIRONMENT_COEFFICIENTS)[k][2])]
    return dict(
        scenario=name, cost_usd=sum(cost_parts.values()), cost_USD=sum(cost_parts.values()),
        cost_interval_usd=[lower,upper], cost_interval_USD=[lower,upper],
        CO2proxy_kg=sum(env_parts.values()), emissions_proxy_kgCO2e=sum(env_parts.values()),
        emissions_proxy_interval_kg=[elower,eupper],
        cost_breakdown_usd=cost_parts, emissions_proxy_breakdown_kg=env_parts,
        cost_feature_quantities=cq, environment_feature_quantities=eq,
        coefficients=c, features=f, derived_features=normalized['derived_features'],
        missing_features=normalized['missing_features'], supplied_feature_vector_complete=not normalized['missing_features'],
        custom_values_outside_illustrative_interval=outside,
        interval_scope='Exact coefficient-box extrema for THIS fixed nonnegative feature vector and the listed terms only; not a confidence interval, empirical total-cost bound, or an interval of globally optimized policies.',
        cost_scope='Undiscounted incremental spending in declared constant-technology USD coefficients; pre-existing elevator capital excluded, new capacity and upkeep included. Wear-life and service renewal require engineering evidence.',
        environment_scope='Selected operational CO2-equivalent proxy only: Earth electricity, R direct-launch benchmark transfer, parameterized R upstream/E propellant/lunar energy. Unmodeled non-CO2 and ecological effects are not set to zero or claimed negligible.',
        future_coefficients_empirically_calibrated=False,
        full_lifecycle_environmental_impact_known=False)


def compare_fixed_plans(features_a, features_b, coefficient='R_flight_services_USD', scenario='central'):
    """Exact one-coefficient crossing of two fixed plans, not reoptimization."""
    if coefficient not in COST_COEFFICIENTS: raise ValueError('Unknown cost coefficient')
    a=evaluate_features(features_a,scenario); b=evaluate_features(features_b,scenario)
    delta_q=a['cost_feature_quantities'][coefficient]-b['cost_feature_quantities'][coefficient]
    coeff=a['coefficients'][coefficient]
    residual=a['cost_usd']-b['cost_usd']-delta_q*coeff
    crossing=None if abs(delta_q)<1e-12 else -residual/delta_q
    differences={k:a['cost_feature_quantities'][k]-b['cost_feature_quantities'][k] for k in COST_COEFFICIENTS}
    dlo=sum(d*(COST_COEFFICIENTS[k][1] if d>=0 else COST_COEFFICIENTS[k][2]) for k,d in differences.items())
    dhi=sum(d*(COST_COEFFICIENTS[k][2] if d>=0 else COST_COEFFICIENTS[k][1]) for k,d in differences.items())
    return dict(coefficient=coefficient, feature_difference=delta_q,
                other_cost_difference_usd=residual, crossing_coefficient=crossing,
                positive_crossing=bool(crossing is not None and crossing>=0),
                cost_a_below_b_for='coefficient below crossing' if delta_q>0 else ('coefficient above crossing' if delta_q<0 else 'coefficient has no effect on difference'),
                exact_difference_interval_usd=[dlo,dhi],
                robust_a_better_for_entire_box=dhi<0,
                separated_individual_intervals=a['cost_interval_usd'][1]<b['cost_interval_usd'][0],
                scope='Fixed-plan comparison holding all other coefficients and both physical plans fixed; a full optimal-policy boundary requires re-solving the candidate catalogue.')


def pareto_frontier(records, cost_key='cost_usd', emission_key='CO2proxy_kg'):
    """Return nondominated record indices for a finite, consistently scored set."""
    vals=[]
    for r in records:
        vals.append((_nonnegative(r[cost_key],cost_key),_nonnegative(r[emission_key],emission_key)))
    return [i for i,(a,b) in enumerate(vals) if not any(c<=a and d<=b and (c<a or d<b) for j,(c,d) in enumerate(vals) if j!=i)]


def epsilon_cost_minimum(records, emissions_budget_kg, cost_key='cost_usd', emission_key='CO2proxy_kg'):
    """Finite-catalogue epsilon constraint; returns None for an empty feasible set."""
    budget=_nonnegative(emissions_budget_kg,'emissions_budget_kg')
    valid=[(i,r) for i,r in enumerate(records) if _nonnegative(r[emission_key],emission_key)<=budget]
    if not valid:return dict(feasible=False,selected_index=None,emissions_budget_kg=budget,scope='No feasible candidate in this finite saved catalogue; not an all-architecture impossibility theorem.')
    i,r=min(valid,key=lambda z:(_nonnegative(z[1][cost_key],cost_key),z[0]))
    return dict(feasible=True,selected_index=i,cost_usd=r[cost_key],CO2proxy_kg=r[emission_key],emissions_budget_kg=budget,scope='Minimum declared scenario cost among saved candidates satisfying the emissions-proxy budget, with all unmodeled environmental dimensions still unresolved.')

