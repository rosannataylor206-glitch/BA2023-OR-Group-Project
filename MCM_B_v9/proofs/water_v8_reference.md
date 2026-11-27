# v8 water guarantee with independently occurring failures

This is an original project derivation for explicitly stated discrete supports.
It is not an empirical lunar reliability result. Time is an integer number of
days. Arrivals, recovery and consumption precede the dispatch decision. One
full batch of net usable water Q may be dispatched on each open opportunity
of a fixed delta-day calendar. The initial usable reserve is r, recovery
backlog and outstanding commitments are zero, and service-loop water G is
accounted separately. The scope of G must be stated by the integrated model.

## 1 Common and independent mechanisms

In every consecutive P-day window let at most R0 common-fault days affect
capture and processing, Rc additional capture-fault days affect capture, and
Rp additional processor-fault days affect processing. These calendars may
overlap and correlate arbitrarily. Capture on a capture-fault day may be
any c in [0,1]; otherwise c=1. Processing on a processor-fault day is zero;
otherwise it is work conserving with recovered-water output at most K.
Consequently union capture days have budget Rcap=R0+Rc and union processor
days have budget Rproc=R0+Rp. Require Rcap<=P and Rproc<P.

For an integer n>=0 define b_b(n)=b floor(n/P)+min(b,n mod P). This is a
safe count envelope for binary event days with rolling budget b. It is
used separately for closed dispatch days B, deadline-settled lost batches J,
and isolated tank incidents T. At most one incident of each class per day
is allowed. A tank event loses actual usable water z<=C, where C is an
absolute compartment capacity, not a fraction of the unknown total reserve.
Isolated quantity loss does not model contaminant propagation or hydraulics.

## 2 Backlog bound without an invalid shared-fault shortcut

The recurrence is Y_t=max(0,Y_(t-1)+eta G c_t-K_t), with K_t=0 on processor
faults and K on normal processing dates. For any busy suffix of length n its
net input is at most eta G n-K(n-b_Rproc(n)). Write n=qP+s. If

    K(P-Rproc)>=eta G P,

the whole-period term is nonpositive. The remainder is at most eta G Rproc:
for s<=Rproc its value is at most eta G s; after Rproc the slope eta G-K is
nonpositive. Therefore Y_t<=Ybar=eta G Rproc, starting from Y_-1=0.

Collection loss on any interval of n days is independently at most
eta G b_Rcap(n). Thus a first valid bound on collection loss on a suffix I
plus Y_t is Esep(n)=eta G[b_Rcap(n)+Rproc]. A new suffix-partition argument
gives a second, often smaller bound without identifying independent faults.

Let J be any reflected-queue suffix ending at t. If J is contained in I,
adding collection loss on I to its candidate backlog leaves collection loss
on I\J. The normal-processing term is nonpositive after writing the result
as eta G Fproc(J)-(K-eta G)(|J|-Fproc(J))+loss(I\J). Common-fault dates in
J and I\J are disjoint subsets of the common dates in I. Processor-only
dates in J and capture-only dates in I\J are bounded by their separate
budgets. The total is therefore no more than
eta G[b_R0(n)+b_Rp(n)+b_Rc(n)]. If I is contained in J, collection loss in I
cancels part of the loss subtracted in the queue candidate, leaving an
expression no greater than Ybar. Taking all J gives

    Epartition(n)=eta G max(Rproc,b_R0(n)+b_Rc(n)+b_Rp(n)).
    E(n)=min(Esep(n),Epartition(n)).

Both are valid bounds on the SAME quantity, so their minimum remains safe.
This is a newly derived partition lemma; the original v7 shared-fault lemma
has not been applied unchanged to independent mechanisms. The sum counts
are still conservative and do not prove the physical minimum. Both terms
and their minimum are nondecreasing in integer n. Increasing K can satisfy
the stability condition and cover larger G, but does not automatically
tighten Ybar. For Rc=Rp=0 and n>=R0, E(n)=eta G b_R0(n), recovering the
original v7 guarantee on its original support.

## 3 Inventory ledger and finite reserve certificate

Retain batch identities and the SAME fixed resolution deadline dispatch+M
for every batch. Successful completed deliveries may occur in [Lmin,M], in
any order; early arrivals are usable immediately. A missing batch is removed
from outstanding commitments P_t only at its fixed deadline and is then
recorded as full loss Q. Early loss telemetry cannot silently change this
accounting clock. No later successful delivery is admitted by this support.

Let H_t accumulate normal net use D=(1-eta)G, capture loss, deadline cargo
loss and actual tank loss; let N_t be cumulative dispatched batches. Then

    IP_t=W_t+Y_t+P_t=r-H_t+QN_t=r-d_t.

Feedback dispatches iff the opportunity is open and pre-dispatch IP<=r-Q.
This uses observed states only and implies d_t>=0. All commitments dispatched
on or before t-M have resolved, giving

    0<=P_t<=Q(N_t-N_(t-M)),
    d_t+P_t<=d_(t-M)+sum_(s=t-M+1)^t (H_s-H_(s-1)).

For a busy interval containing n days and one opportunity every delta days,
at least floor(n/delta)-b_B(n) opportunities survive the closure budget;
negative values are replaced by zero. Define

    A(n)=Dn+E(n)+Q b_J(n)+C b_T(n),
    S(n)=Q max(0,floor(n/delta)-b_B(n)).

With daily review a sufficient reserve is

    r8=Q+sup_(n>=M) [A(n)-S(n-M)].

Proof: let e=t-M and find the latest u<=e with d_u<Q (u=-1 is available at
startup). All open opportunities in (u,e] are used. Writing n=t-u, the
commitment inequality, the busy-interval service bound and the external-loss
envelope give d_t+P_t+Y_t<Q+A(n)-S(n-M)<=r8. Thus W_t>=0. For t<M,
P_t<=QN_t gives d_t+P_t+Y_t<=A(t+1)<=A(M)<=r8. Monotonicity here follows
from nonnegative D and the proved nondecreasing E and count envelopes. Since IP<=r
and P,Y>=0, W_t<=r at day end. With review period p, conservative waiting
p-1 shifts M to M+p-1 in the same busy-period argument.

The strictly positive transport slack required here is

    m=Q(1/delta-B/P)-D-eta G Rcap/P-QJ/P-CT/P>0.

Let a=1/delta-B/P>0, n0=ceil((1+B)/a), and H=lcm(P,delta). Once
n>=M+n0, the service positive part is inactive. If Rp>0, define
Nswitch=P ceil(Rproc/Rp). For n>=Nswitch, b_Rp(n)>=Rproc and
b_R0(n)+b_Rc(n)>=b_Rcap(n), so Epartition>=Esep and E=Esep. If Rp=0,
then for n>=P the maximum in Epartition is inactive. The excess
b_R0(n)+b_Rc(n)-b_Rcap(n) lies between 0 and R0=Rproc; thus
E=eta G[b_R0(n)+b_Rc(n)] and has the same capture-rate period increment.
Use Nswitch=P in this case. Therefore beyond
Nstart=max(M+n0,Nswitch), increasing n by H decreases A(n)-S(n-M)
by exactly Hm. It suffices to scan M through Nstart+H. No monotonicity of
S is presumed. Failure of these sufficient conditions does not by itself
prove every possible policy infeasible.

## 4 Complete receiving-port closures

Upstream transport completion before receiving has lag [l,u]. At most one
batch is dispatched every delta days, so any n consecutive raw-arrival days
contain at most alpha(n)=ceil((n+u-l)/delta) batches. The receiver starts
empty and is FIFO and work conserving: on each open day it handles min(m,
queue) whole flights; on closed days it handles zero. In any P consecutive
days at most Brx days are completely closed.

Immediately before today's service, a continuously busy suffix of n days
has at most

    alpha(n)-m[(n-1)-b_Brx(n-1)]

queued jobs. Taking the supremum over n>=1 bounds the pre-service queue.
For H=lcm(P,delta), increasing n by H changes this expression by
H/delta-mH(1-Brx/P). Under strict receiver slack m(1-Brx/P)>1/delta the
change is negative for every n>=1. Hence its supremum is attained among
n=1,...,H. Let the resulting bound be Bq.

Choose the smallest positive h with m[h-b_Brx(h)]>=Bq. In h dates starting
on an arrival date the FIFO receiver can serve every job preceding that
arrival plus the arrival itself; later arrivals cannot overtake it. The
last possible completion is arrival+h-1, so M=u+h-1 is sufficient. Such an h
exists, and h<=P ceil(Bq/[m(P-Brx)]). Arrival-date service is counted once.
This separately bounding queue and subsequent service is conservative: the
maximal queue and maximal future closure run need not be jointly attainable.
Closure calendars may correlate with dispatch, process and capture faults.

The receiving formula handles complete port closures only within the
specified finite rolling budget. It does not cover an unbounded port outage.

## 5 Capacity modules and finite permanent-hull-loss resources

For G<=Gmax and at most s processor modules simultaneously unavailable,
each remaining module supplying k tonnes/day, install

    n=s+ceil(eta Gmax P/[k(P-Rproc)]).

Then K=(n-s)k satisfies the processing condition even while those s modules
are unavailable and the processor calendar has Rproc full outages. Module
mass, power, price, disinfection, temperature and partial-gravity performance
are separate engineering inputs. A capacity unit of 25 tonnes/day is a
declared modular design unit, not a measured NASA future plant specification.

For a finite dispatch horizon T days, at most b_H(T) permanently lost hulls
can originate from the dispatches if losses have binary dispatch-date rolling
budget H per P days. Assume every normal hull returns, or its permanent loss
is recognized, within Ccycle days. A ready spare initially at the dispatch
side can be activated within a days. Reserve F0=ceil((Ccycle+a)/delta)
rotation slots and hold each normally returning hull until its assigned slot
is reused. The next use is at least F0 delta>=Ccycle+a days after departure.
A lost hull is therefore replaced before its next slot. With b_H(T) spare
hulls initially available, every replacement through the modeled dispatch
horizon and its resolution tail is possible. Cargo losses remain subject to
their separate J envelope.

These spares are a finite stock. The argument does not guarantee unlimited
years from one year's stock. Initial deployment mass belongs at the dispatch
location: an apex spare must be lifted but is not necessarily landed on the
Moon. Actual hull loss probabilities, spare manufacture and activation
performance remain design assumptions requiring engineering evidence.

## 6 Storage and interpretation

One working day of G is separate from the reserve r. Receiving/recovery can
precede consumption, so a conservative usable-fresh peak capacity is r+G.
With isolated compartments C, <=T incidents per P days, all initially intact,
and repairs completed within P days before same-day new incidents, at most T
compartments are disabled. Installing ceil((r+G)/C)+T guarantees aggregate
quantity capacity, conditional on functioning isolation and access. The
simulation uses bounded quantity loss and aggregate capacity; it is not a
per-compartment hydraulic, pressure, mixing or water-quality simulation.

All guarantees above concern the declared day grid and quantity states.
The integrated model must separately reserve transportation and receiving
resources for construction, initial water, replacement hull deployment,
processor modules and their operating resources. Counting the same slots
twice invalidates the physical interpretation even if this submodel passes.
