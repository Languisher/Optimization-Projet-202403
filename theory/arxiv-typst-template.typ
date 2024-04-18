#import "@preview/arkheion:0.1.0": arkheion, arkheion-appendices

#show: arkheion.with(
  title: "Application of the Pontryagin's Minimum Principle",
  authors: (
    (name: "Nan Lin", email: "lns_brandon@sjtu.edu.cn", affiliation: "Shanghai Jiao Tong University", orcid: "0009-0009-0430-7855"),
  ),
  // Insert your abstract after the colon, wrapped in brackets.
  // Example: `abstract: [This is my abstract...]`
  abstract: lorem(55),
  keywords: ("Optimization", "Control System", "Pontryagin's Minimum Principle"),
  date: "May 16, 2023",
)

#pagebreak()

= Background Information 

== Finite-dimensional Optimization 

Consider a function $f :RR^n -> RR$, and $||.||$ is an Euclidean norm on $RR^n$. A point $x^*$ is a *local minimum* of function $f$ in it's definition domain, denoted as $D_f$, if there exists an constant $delta >0$ such that, $ forall x in D, quad |x-x^*| < delta, quad f(x^*) <= f(x) $

=== Unconstrained Optimization

We have the sufficient condition for optimality: if $f$ is a twice continously differentiable function, and on the point $x^* in D_f$ we have $ cases(nabla f(x^*) &= 0, nabla^2 f(x^*) &= 0 quad  ("positively definite")) $

Therefore, $x^*$ is a local minimum of function $f$. Detailed demonstration of this theorem can be found in any _Optimization_ course.

=== Constrained Optimization <3>

Now we add constraints to $D_f$, which is defined by the equality constraints: $ forall x in D_f, quad h_1 (x) = dots = h_m (x) = 0 $

Suppose that $x^* in D_f$ is a local minimum of $f$ and a regular point of $D$. From the definition, the gradients at $x^*$ ($nabla h_(i in [1, m])$) are linearly independent.

Therefore,  $ nabla f(x^*) in "span"{nabla h_i (x^*), quad i = 1, dots, m} $

It is equivlant to say that $ exists (lambda_1^*, dots, lambda_m^*) in RR^m, quad nabla f(x^*) + sum_(j=1)^m lambda_j nabla h_j (x^*) = 0 $

We name $lambda = mat(lambda_1, dots, lambda_m)^T$ *Lagrange multipliers*.

The above equation can be decomposed into: $ forall i in [1,m], quad (frac(partial f(x), partial x_i) + sum_(j=1)^m frac(partial h_j (x), partial x_i))|_(x = x^*) = 0 $

Now, consider the *augmented cost function* $F: RR^n times RR^m -> RR$, defined by : $ F(x, lambda) = f(x) + sum_(i=1)^m lambda_i h_i (x) $

If $(x^*, lambda^*)$ resp. the local constrained minimum and the coressponding vector of Lagrange multipliers, then the gradient of $F$ at $(x^*, lambda^*)$ satisfies $ nabla F(x,lambda)|_(x=x^*, lambda = lambda^*) = mat(F_x (x, lambda)|_(x=x^*, lambda=lambda^*);F_lambda (x, lambda)|_(x=x^*, lambda=lambda^*)) = mat(nabla f(x^*) + sum_(j=1)^m lambda_j^* nabla h_j(x^*); h(x^*)) = 0  $

The above condition in terms of Lagrange multipliers is  necessary but not sufficient for constrained optimality.

== Local minima of a functional 

First we define a *functional*, which could be thought as a "function of a function". If there exist a one-to-one mapping between a variable quantity $J$ and a function $y(t)$, then $J$ is a functional denoted as $J[y(t)]$.

For example, in @2 we have $ J = integral_(t_0)^(t_f) L(t, x, u)" d"t $ Here $J$ is a functional of $L$ denoted as $J[L(t, x, u)]$.


In this part, we are going to formally define *local minima of a functional*. Suppose $V$ a function space with norm $||.||_p$. A _function_ (not a variable !!) is a local minimum of $J$ over a subset of $V$ denoted as $A$, which is a real-valued functional defined on $V$, if $ exists epsilon > 0, quad forall y in A, quad ||y-y^*||_p<= epsilon quad ==> quad J(y^*) <= J (y) $

== Controled Dynamic <1>

Consider an _ordinary differential equation (ODE)_ as follows $ cases(dot(x)(t) = f(x(t)) quad t > 0, x(0) = x_0) $

The unknown is the "curve" of the dynamical evolution of a certain "system" $x :[0, t_f]->RR^n$, where $t_f$ is the end of the time length.

Now, the function $f$ also depends upon some control parameters belonging to a set $A subset RR^m$, named as *collection of all admissible controls*. If these control parameters are time-variant, we consider the ODE $ cases(dot(x)(t) = f(x(t), u(t)) quad t>0, x(0) = x_0) $

== Euler-Lagrange Equation <4>

#pagebreak()


= Optimal Control

== Optimal Control Problem <2>

=== Formulation

Based on the ODE Equation on @1: $ dot(x)(t) = f(x, u, t), quad x(t_0) = x_0 $ 
We need another ingredient for the _Optimal Control Problem_: the *cost functional*, denoted as $J(u)$, which assigns a cost value to each admissible control. It can be written as: $ J(u) eq.def integral_(t_0)^(t_f) L(t, x(t), u(t))" d"t + phi(t_f, x_f (t_f)) $

where the first term is the running cost, or the *Lagrangian*, depending on the time, and the second term is ther terminal cost, only taking account of the final state.

For example, if we want to minimize the time-consume of a certain system, like a marathon race, the cost functional could be expressed as $ J(u) = integral_(t_0)^(t_f) 1" d"t $

To formulate the optimal control problem, we follow the steps:
+ Establish the state equation $dot(x) = f(x(t), u(t), t)$
+ Clarify the boundary conditions $x(t_0) = x_0, x(t_f) in S$
+ Defining the performance index $J$
+ Confirming the admissible range $u(t) in Omega$, then add it to the state equations if needed (will be introduced in the later sections)

=== Analysis

#set text(fill: red)

In this section and the following section, we suppose that the control variable are free and is not limited by any equality or inequality constraint.

#set text(fill: black)

Our aim is to minimize the cost functional under the system expressed as $ dot(x)(t) = f(x(t), u(t), t) quad <==> quad f(x(t), u(t), t)- dot(x)(t) = 0 $

It could be conceptualized as minimizing $J$ under the constraint of the equation above. In this case, we can use the method introduced in @3.

Suppose that $x$ is an $n$-dimensional state vector, in accordance, we introduce an $n$-dimensional _Lagrange vector_ $lambda(t) = mat(lambda_1 (t), dots, lambda_n (t))^T$ to obtain the _augmented functional_ $J_"aug"$: $ J_"aug" = phi(x(t_f), t_f) + integral_(t_0)^(t_f) (L(x(t), u(t), t) + lambda^T (t)[f(x(t), u(t), t) - dot(x)(t)])" d"t $

By introducing an auxiliary function which is also called *Hamilton function* defined as $ H(x, u, lambda, t) eq.def L(x, u, t) + lambda^T f(x, u, t) $

The above formula could be written as $ J_"aug" = phi(x(t_f), t_f) + integral_(t_0)^(t_f) (H(x, u, lambda, t) - lambda^T dot(x))" d"t $

From the *Euler-Lagrange Equation* of the functional $J_"aug"$, deduced from @4, we can obtain the necessary conditions for the unconstraint optimal problem: $ lambda(t_f) = display(frac(partial phi, partial x(t_f))) \  dot(lambda) = - display(frac(partial H, partial x)) \ display(frac(partial H, partial u)) = 0 $

Meanwhile, the system state equation could be written a more compact form: $ dot(x) = frac(partial H, partial lambda) $

=== Solution

The above analysis can be concluded as the *theorem*: If the control system $ dot(x)(t) = f(x, u, t), quad x(t_0) =x_0 $ can make the performance index functional $ J = phi(x(t_f), t_f) + integral_(t_0)^(t_f) L(x(t), u(t), t)" d"t $ at a fixed-end-time $t_f$ and a _free_-end-state $x(t_f)$. Then the following conditions and equations should hold simultaneously: 
- The *boundary conditions* $ lambda(t_f) = frac(partial phi, partial x(t_f)), quad x(t_0) = x_0 $
- The *control equation* $ frac(partial H, partial u)|_(u=u^*) = 0 $
- The *canonical equations* $ dot(lambda) = - frac(partial H, partial x), quad dot(x) = frac(partial H, partial lambda) $

Therefore, the procedure to solve the constraint functional extrema is divided into three steps:
+ From $J$, derive $L$ and $phi$.
+ Give _Hamilton function_ $ H = L + lambda^T f $
+ Get the expression of the optimal control $u^* = u^*(x, lambda)$ from the *control equation* 
+ Substitute $u^*$ into the *canonical equations*, use the *boundary conditions* to obtain the optimal state trajectory $x^*$ and adjoint state trajectory $lambda^*$
+ Substitute $x^*$ and $lambda^*$ into $u^*$ to obtain the optimal control.


#pagebreak()

=  The Pontryagin's aMaximum/Minimum Principle

#pagebreak()

= Problem Formulation

== State and Control

In this study, we analyze the dynamics of an electric vehicle (EV) navigating a real-world environment. Let $s(t)∈RR$ represent the cumulative distance traveled by the vehicle at time $t$, and $v(t)∈ RR$ denote its velocity. Furthermore, the vehicle's total energy at any given moment is expressed as $w(t)∈ RR$.

The operation of the EV is subject to several physical constraints:
- The speed of the vehicle $v(t)$ could not exceed a certain amount denoted as $v_"max"$,
- The vehicle's total energy is bounded by an upper limit, thus constrained to the condition that $|w(t)| <= E_"max"$,
- The output power of the vhicle is also limited, thus, $|p(t)| <= P_"max"$


The control set, denoted as $cal(U)$ is a compact and convex subset of $RR^3$.

Let's define the state and the control $ bold(x)(t) &= mat(s(t), v(t), w(t))^T in RR^3 \ bold(u) (t) &= mat(v(t), w(t), p(t) )^T in cal(U) $

== Physical Analysis

Physical model implies the following consequences:

1) *The relation between the distance and the speed*, where $t_0$ and $t_f$ are respectively the beginning time and the ending time: $ v(t) = frac(" d"s(t), " d"t), quad s(t) = s_0 + integral_(t_0)^(t_f) v(t)" d"t $

2) *The relation between the accerleration and the power also the vitesse of the vehicle*, where the first term derives from the motor force, the second term derives from the friction, $theta$ denotes the inclination of the road and $mu$ is the friction coefficient. The third force is the force of air resistence, $rho$ is the air density, $C_d$ is the air resistence coefficient and $A$ is the surface of the vehicle.

$ frac(" d"v(t), " d"t) = frac(p(t), v(t)) -m g(sin theta+ mu cos theta) - 1/2 rho C_d A v^2(t) $

3) *The relation between the total energy (left) of the vehicle and its power output, in the meantime take in account of its power recupation.*

== Dynamic of the System

For a admissible control $u in cal(U)$, the dynamics of the system is described by the following equation: $ forall t >= 0, quad bold(dot(x))(t) = f(bold(x)(t), bold(u)(t)) $