# v9 Fixed-capacity construction certificate

This is a deterministic sufficient policy, not unrestricted engineering
optimization. The main capacity baseline fixes three harbours, each with
179,000 gross tonnes/year, and ten selected rocket sites. The 250 nominal
flights/site/year, receiving ratings, calendars and future mission performance
are named scenarios. Warehouse and terminal capacities are design outputs;
an optional explicit engineering-capacity stress is separate.

## 1 Physical sources and service curves

All three E sources and all ten R sources are balanced within each route.
At most one E mission per delta=2 days is assigned to each harbour. Two full
R receiving slots per physical site and one per E harbour are reserved.
Each actual flight is checked at its gross touchdown mass, not its mean flow.
Terminal modules are procured to meet the simultaneous full-flight burst.

For every interval of n integer days the number of closed dates is bounded by

    b_B(n)=B floor(n/P)+min(B,n mod P) <= Bn/P+B.

A fluid stage with open-day capacity c has rate c(1-B/P) and latency
B/(1-B/P)+1. The extra day embeds its discrete right-continuous cumulative
service in continuous time. An opportunity stage with one packet of mass Q
every delta days has conservative rate Q(1/delta-B/P) and latency
(1+B)/(1/delta-B/P)+1. For R the balanced periodic 250/site/year nominal
calendar gives at least floor(250n/P) opportunities; B fault dates remove at
most B additional opportunities, producing rate Q(250-B)/P and the same
packet-calendar construction. A floor bound for every interval is part of
this balanced-calendar scenario, not a measured launch calendar.

Convolution of the stages gives the minimum rate r and sum latency T.
The source is regulated at rate r and packetized. Four Q per physical source
are deducted for the source/intermediate/final packetization boundaries.
There is no unbounded input burst. If the source is open for d days and is
stopped by H-T, then at least rd-4Q of attempts have been settled by H.

## 2 Cargo destruction is not merely a closed date

Each attempted full mission is charged at full payload Q and full recurring
propellant. A failed cargo mission is a lost physical payload. To retain the
same conservative service accounting, it is coupled to a virtual full job at
the maximum arrival deadline and consumes its reserved receiving service.
Removing a failed physical job cannot worsen that virtual FIFO schedule.
Cargo-loss accounting is therefore separate from calendar stoppages:

    useful delivered by H >= rd-4Q-Q b_j(H).

The rolling loss budget is indexed by dispatch date, at most one lost batch
per source per date. Hull losses before landing must be included among these
cargo losses; a return-leg hull loss need not lose delivered cargo. The proof
permits a conservative superset of these correlations. This guarantee does
not assume that the loss happens before dispatch or preserves the cargo.

## 3 Permanent hull losses and initial deployment

For each E harbour, the individually bounded receiving queue gives a completed
delivery deadline M. Let Rtail be the independently rounded upper bound on the
physical return tail supplied by the trajectory interface, and set C=M+Rtail.
Subtracting two separately rounded cycle/outbound upper bounds would be invalid.
Every intact hull returns or its permanent
loss is confirmed within C. A ready spare is activated within a days.

    F0=ceil((C+a)/delta).

The next use of a rotation slot is no earlier than F0*delta, so a lost hull can
be replaced before that slot is used. All ready spares are physically deployed
at the same harbour before any construction cargo is released. For a candidate
horizon H, allocate

    S(H)=ceil(hH/P+h) >= b_h(H).

No instant towing or spare transfer between harbours is assumed. If A intact
hulls per harbour are already guaranteed from an earlier phase, only
max(0,F0-A)+S new hulls are purchased and lifted. Initial warehouse design
counts max(A,F0)+S hulls, and root orchestration additionally carries every
possibly unconsumed older spare as a storage upper bound. Lost dry
structure is never recovered for free. After final settlement and the full
return/activation wait, exactly the F0 occupied rotation slots are guaranteed
intact (or A when A>F0); unused spares are not credited as available service
capacity in the next phase.

## 4 A monotone horizon certificate despite integer loss budgets

Directly solving rd(H)-Q b_j(H)>=m by bisection would be wrong: b_j and
integer hull stocks have upward steps. Instead, use an affine lower bound.
Let z=chi Q be dry mass per E hull, L the effective gross lift rate, and

    S(H) <= hH/P+h+1  (h>0),  S=0 (h=0).
    A_aff(H)=Tlift+climber+[max(0,F0-A)+hH/P+h+1]z/L+1 = a0+a1 H.

The final +1 day pays for integer deployment rounding. For h=0 the h+1 spare
term is removed. If no new base or spare hulls are needed, deployment is zero.
The physical deployment time is the ceiling of lift latency,
climber transit and integer hull mass/L, and is no greater than A_aff(H).
Set d=floor(H-deployment-T). Thus

    d >= H-A_aff(H)-T-1.

Using b_j(H)<=jH/P+j gives

    useful/source >= [r(1-a1)-Qj/P]H
                       -[r(a0+T+1)+4Q+Qj] = vH-k.

For R take a0=a1=0. If v<=0, this policy does not certify sustained delivery.
For v>0, choose the integer horizon

    H=ceil((m+k)/v).

This is a genuinely increasing affine sufficient bound. Code then reconstructs
the integer spare count, actual initial deployment, finite source duration,
full packet attempts and exact rolling cargo/hull budgets; it checks the exact
bound is no smaller than the affine certificate and the allocated target.
No H-dependent staircase is silently treated as monotone. This formula proves
a feasible upper time, not the shortest feasible horizon over all schedules.

## 5 Full attempts, finite storage and phase handoff

The source pays N=ceil(rd/Q) full attempts per physical source, so
0<=NQ-rd<Q (up to exact equality). The complete E mass newly lifted is

    g NQ + chi Q(max(0,F0-A)+S),
    g=1+(beta-chi-1)/(1-lambda).

The dry fleet is lifted once before construction; each attempt lifts cargo and
propellant. Lambda bounds fractional propellant loss between loading and use;
it is not a daily loss compounded across the construction centuries.
All full source attempts are charged even if their cargo is destroyed or
their final rounding is surplus. Ground attempts are charged as full rockets.

An apex storage design bound per harbour is

    g[r(Tlift+Tdispatch)+2Q]+chi Q(max(A,F0)+S).

Integer warehouse packages are rounded separately per physical harbour.
Their total is not a pool from which cargo teleports between apexes. The bound
includes all predeployed spare structure and regulated-stream bursts.

In the virtual settled-job network, NQ-(rd-4Q)<=5Q. Therefore no more than
five complete jobs remain unsettled at H. Stop ALL actual rocket departures
at H; no residual cargo is launched during handoff. Failed cargo and hull-loss
budgets therefore apply only to dispatch dates <=H, including the resolution
tail of those same attempts. Upstream residual is retained as quarantined
inventory: at most 5Q per physical source, or g*5Q gross at each E apex.
Ground residual remains on Earth. No next-phase cargo credit is taken.

Any pre-H flight completes receiving within its individually proved M, then
an E hull returns/gets replaced within Rtail+a. Residual climbing cargo reaches
the apex within Tlift+climber+6Q/r; all residual thereafter stays quarantined.
Thus a sufficient handoff wait is

    wait_E=max(Tlift+climber+6Q_E/r_E, M_E+Rtail+a),
    wait_R=M_R.

The full allocated N source jobs are charged as a conservative upper bound on
actual launches, even if some are held unlaunched at the cutoff. Result fields
state this upper-count identity explicitly. This is deliberate safe overcharge,
not a claim that held cargo was physically launched or lost. A direct post-H
launch flush without extending cargo and hull budgets would be invalid.

The two routes start in parallel. Their construction-completion upper time is
max(H_E,H_R). Water prepositioning starts after max(H_E+wait_E,H_R+wait_R).
Quarantine capacity remains reserved through later phases, in addition to
their active inventories. Cargo already destroyed is settled loss, not a
material queue to be drained.

## 6 Truth and boundaries

The ideal and fault cases use exactly the same lift and site capacities; ideal
sets outage/loss budgets and retention loss to zero. There is no compulsory
50-year deadline, no integer multiplier of the official lift capacity, and no
claim that an uncalibrated future launch schedule is observed data. Any share
catalogue optimization is restricted to its saved finite policy choices.

Times of hundreds of years under a fixed 2050 technology scenario are conditional
stress results, not forecasts of actual vehicle longevity or society. Age-related
retirement, parked-vehicle degradation and technology change are not calibrated.
The model covers explicitly budgeted flight hull loss and cargo destruction;
it cannot guarantee against arbitrary catastrophic harbour destruction,
unbounded contamination, or failures outside the stated supports.
