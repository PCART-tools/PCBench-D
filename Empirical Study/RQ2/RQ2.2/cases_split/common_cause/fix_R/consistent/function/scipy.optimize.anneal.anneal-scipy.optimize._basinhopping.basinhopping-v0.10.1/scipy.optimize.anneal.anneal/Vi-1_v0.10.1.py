
# TODO:
#     allow for general annealing temperature profile
#     in that case use update given by alpha and omega and
#     variation of all previous updates and temperature?

# Simulated annealing

def anneal(func, x0, args=(), schedule='fast', full_output=0,
           T0=None, Tf=1e-12, maxeval=None, maxaccept=None, maxiter=400,
           boltzmann=1.0, learn_rate=0.5, feps=1e-6, quench=1.0, m=1.0, n=1.0,
           lower=-100, upper=100, dwell=50):
    """Minimize a function using simulated annealing.

    Schedule is a schedule class implementing the annealing schedule.
    Available ones are 'fast', 'cauchy', 'boltzmann'

    Parameters
    ----------
    func : callable f(x, *args)
        Function to be optimized.
    x0 : ndarray
        Initial guess.
    args : tuple
        Extra parameters to `func`.
    schedule : base_schedule
        Annealing schedule to use (a class).
    full_output : bool
        Whether to return optional outputs.
    T0 : float
        Initial Temperature (estimated as 1.2 times the largest
        cost-function deviation over random points in the range).
    Tf : float
        Final goal temperature.
    maxeval : int
        Maximum function evaluations.
    maxaccept : int
        Maximum changes to accept.
    maxiter : int
        Maximum cooling iterations.
    learn_rate : float
        Scale constant for adjusting guesses.
    boltzmann : float
        Boltzmann constant in acceptance test
        (increase for less stringent test at each temperature).
    feps : float
        Stopping relative error tolerance for the function value in
        last four coolings.
    quench, m, n : float
        Parameters to alter fast_sa schedule.
    lower, upper : float or ndarray
        Lower and upper bounds on `x`.
    dwell : int
        The number of times to search the space at each temperature.

    Returns
    -------
    xmin : ndarray
        Point giving smallest value found.
    Jmin : float
        Minimum value of function found.
    T : float
        Final temperature.
    feval : int
        Number of function evaluations.
    iters : int
        Number of cooling iterations.
    accept : int
        Number of tests accepted.
    retval : int
        Flag indicating stopping condition::

                0 : Points no longer changing
                1 : Cooled to final temperature
                2 : Maximum function evaluations
                3 : Maximum cooling iterations reached
                4 : Maximum accepted query locations reached
                5 : Final point not the minimum amongst encountered points

    Notes
    -----
    Simulated annealing is a random algorithm which uses no derivative
    information from the function being optimized. In practice it has
    been more useful in discrete optimization than continuous
    optimization, as there are usually better algorithms for continuous
    optimization problems.

    Some experimentation by trying the difference temperature
    schedules and altering their parameters is likely required to
    obtain good performance.

    The randomness in the algorithm comes from random sampling in numpy.
    To obtain the same results you can call numpy.random.seed with the
    same seed immediately before calling scipy.optimize.anneal.

    We give a brief description of how the three temperature schedules
    generate new points and vary their temperature. Temperatures are
    only updated with iterations in the outer loop. The inner loop is
    over loop over xrange(dwell), and new points are generated for
    every iteration in the inner loop. (Though whether the proposed
    new points are accepted is probabilistic.)

    For readability, let d denote the dimension of the inputs to func.
    Also, let x_old denote the previous state, and k denote the
    iteration number of the outer loop. All other variables not
    defined below are input variables to scipy.optimize.anneal itself.

    In the 'fast' schedule the updates are ::

        u ~ Uniform(0, 1, size=d)
        y = sgn(u - 0.5) * T * ((1+ 1/T)**abs(2u-1) -1.0)
        xc = y * (upper - lower)
        x_new = x_old + xc

        c = n * exp(-n * quench)
        T_new = T0 * exp(-c * k**quench)


    In the 'cauchy' schedule the updates are ::

        u ~ Uniform(-pi/2, pi/2, size=d)
        xc = learn_rate * T * tan(u)
        x_new = x_old + xc

        T_new = T0 / (1+k)

    In the 'boltzmann' schedule the updates are ::

        std = minimum( sqrt(T) * ones(d), (upper-lower) / (3*learn_rate) )
        y ~ Normal(0, std, size=d)
        x_new = x_old + learn_rate * y

        T_new = T0 / log(1+k)

    """
    x0 = asarray(x0)
    lower = asarray(lower)
    upper = asarray(upper)

    schedule = eval(schedule+'_sa()')
    #   initialize the schedule
    schedule.init(dims=shape(x0),func=func,args=args,boltzmann=boltzmann,T0=T0,
                  learn_rate=learn_rate, lower=lower, upper=upper,
                  m=m, n=n, quench=quench, dwell=dwell)

    current_state, last_state, best_state = _state(), _state(), _state()
    if T0 is None:
        x0 = schedule.getstart_temp(best_state)
    else:
        best_state.x = None
        best_state.cost = numpy.Inf

    last_state.x = asarray(x0).copy()
    fval = func(x0,*args)
    schedule.feval += 1
    last_state.cost = fval
    if last_state.cost < best_state.cost:
        best_state.cost = fval
        best_state.x = asarray(x0).copy()
    schedule.T = schedule.T0
    fqueue = [100, 300, 500, 700]
    iters = 0
    while 1:
        for n in xrange(dwell):
            current_state.x = schedule.update_guess(last_state.x)
            current_state.cost = func(current_state.x,*args)
            schedule.feval += 1

            dE = current_state.cost - last_state.cost
            if schedule.accept_test(dE):
                last_state.x = current_state.x.copy()
                last_state.cost = current_state.cost
                if last_state.cost < best_state.cost:
                    best_state.x = last_state.x.copy()
                    best_state.cost = last_state.cost
        schedule.update_temp()
        iters += 1
        # Stopping conditions
        # 0) last saved values of f from each cooling step
        #     are all very similar (effectively cooled)
        # 1) Tf is set and we are below it
        # 2) maxeval is set and we are past it
        # 3) maxiter is set and we are past it
        # 4) maxaccept is set and we are past it

        fqueue.append(squeeze(last_state.cost))
        fqueue.pop(0)
        af = asarray(fqueue)*1.0
        if all(abs((af-af[0])/af[0]) < feps):
            retval = 0
            if abs(af[-1]-best_state.cost) > feps*10:
                retval = 5
                print "Warning: Cooled to %f at %s but this is not" \
                      % (squeeze(last_state.cost), str(squeeze(last_state.x))) \
                      + " the smallest point found."
            break
        if (Tf is not None) and (schedule.T < Tf):
            retval = 1
            break
        if (maxeval is not None) and (schedule.feval > maxeval):
            retval = 2
            break
        if (iters > maxiter):
            print "Warning: Maximum number of iterations exceeded."
            retval = 3
            break
        if (maxaccept is not None) and (schedule.accepted > maxaccept):
            retval = 4
            break

    if full_output:
        return best_state.x, best_state.cost, schedule.T, \
               schedule.feval, iters, schedule.accepted, retval
    else:
        return best_state.x, retval
