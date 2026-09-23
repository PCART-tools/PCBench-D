
# TODO:
#     allow for general annealing temperature profile
#     in that case use update given by alpha and omega and
#     variation of all previous updates and temperature?

# Simulated annealing

def anneal(func, x0, args=(), schedule='fast', full_output=0,
           T0=None, Tf=1e-12, maxeval=None, maxaccept=None, maxiter=400,
           boltzmann=1.0, learn_rate=0.5, feps=1e-6, quench=1.0, m=1.0, n=1.0,
           lower=-100, upper=100, dwell=50, disp=True):
    """Minimize a function using simulated annealing.

    Schedule is a schedule class implementing the annealing schedule.
    Available ones are 'fast', 'cauchy', 'boltzmann'

    Parameters
    ----------
    func : callable ``f(x, *args)``
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
    disp : bool
        Set to True to print convergence messages.

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

    See also
    --------
    minimize: Interface to minimization algorithms for multivariate
        functions. See the 'Anneal' `method` in particular.

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

    opts = {'schedule'  : schedule,
            'T0'        : T0,
            'Tf'        : Tf,
            'maxfev'    : maxeval,
            'maxaccept' : maxaccept,
            'maxiter'   : maxiter,
            'boltzmann' : boltzmann,
            'learn_rate': learn_rate,
            'ftol'      : feps,
            'quench'    : quench,
            'm'         : m,
            'n'         : n,
            'lower'     : lower,
            'upper'     : upper,
            'dwell'     : dwell,
            'disp'      : disp}

    res = _minimize_anneal(func, x0, args, **opts)

    if full_output:
        return res['x'], res['fun'], res['T'], res['nfev'], res['nit'], \
            res['accept'], res['status']
    else:
        return res['x'], res['status']
