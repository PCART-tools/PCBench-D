def anneal(func, x0, args=(), schedule='fast', full_output=0,
           T0=None, Tf=1e-12, maxeval=None, maxaccept=None, maxiter=400,
           boltzmann=1.0, learn_rate=0.5, feps=1e-6, quench=1.0, m=1.0, n=1.0,
           lower=-100, upper=100, dwell=50, disp=True):
    """
    Minimize a function using simulated annealing.

    Uses simulated annealing, a random algorithm that uses no derivative
    information from the function being optimized. Other names for this
    family of approaches include: "Monte Carlo", "Metropolis",
    "Metropolis-Hastings", `etc`. They all involve (a) evaluating the
    objective function on a random set of points, (b) keeping those that
    pass their randomized evaluation critera, (c) cooling (`i.e.`,
    tightening) the evaluation critera, and (d) repeating until their
    termination critera are met.  In practice they have been used mainly in
    discrete rather than in continuous optimization.

    Available annealing schedules are 'fast', 'cauchy' and 'boltzmann'.

    Parameters
    ----------
    func : callable
        The objective function to be minimized.  Must be in the form
        `f(x, *args)`, where `x` is the argument in the form of a 1-D array
        and `args` is a  tuple of any additional fixed parameters needed to
        completely specify the function.
    x0: 1-D array
        An initial guess at the optimizing argument of `func`.
    args : tuple, optional
        Any additional fixed parameters needed to completely
        specify the objective function.
    schedule : str, optional
        The annealing schedule to use.  Must be one of 'fast', 'cauchy' or
        'boltzmann'.  See `Notes`.
    full_output : bool, optional
        If `full_output`, then return all values listed in the Returns
        section. Otherwise, return just the `xmin` and `status` values.
    T0 : float, optional
        The initial "temperature".  If None, then estimate it as 1.2 times
        the largest cost-function deviation over random points in the
        box-shaped region specified by the `lower, upper` input parameters.
    Tf : float, optional
        Final goal temperature.  Cease iterations if the temperature
        falls below `Tf`.
    maxeval : int, optional
        Cease iterations if the number of function evaluations exceeds
        `maxeval`.
    maxaccept : int, optional
        Cease iterations if the number of points accepted exceeds `maxaccept`.
        See `Notes` for the probabilistic acceptance criteria used.
    maxiter : int, optional
        Cease iterations if the number of cooling iterations exceeds `maxiter`.
    learn_rate : float, optional
        Scale constant for tuning the probabilistc acceptance criteria.
    boltzmann : float, optional
        Boltzmann constant in the probabilistic acceptance criteria
        (increase for less stringent criteria at each temperature).
    feps : float, optional
        Cease iterations if the relative errors in the function value over the
        last four coolings is below `feps`.
    quench, m, n : floats, optional
        Parameters to alter the `fast` simulated annealing schedule.
        See `Notes`.
    lower, upper : floats or 1-D arrays, optional
        Lower and upper bounds on the argument `x`.  If floats are provided,
        they apply to all components of `x`.
    dwell : int, optional
        The number of times to execute the inner loop at each value of the
        temperature.  See `Notes`.
    disp : bool, optional
        Print a descriptive convergence message if True.

    Returns
    -------
    xmin : ndarray
        The point where the lowest function value was found.
    Jmin : float
        The objective function value at `xmin`.
    T : float
        The temperature at termination of the iterations.
    feval : int
        Number of function evaluations used.
    iters : int
        Number of cooling iterations used.
    accept : int
        Number of tests accepted.
    status : int
        A code indicating the reason for termination:

        - 0 : Points no longer changing.
        - 1 : Cooled to final temperature.
        - 2 : Maximum function evaluations reached.
        - 3 : Maximum cooling iterations reached.
        - 4 : Maximum accepted query locations reached.
        - 5 : Final point not the minimum amongst encountered points.

    See Also
    --------
    basinhopping : another (more performant) global optimizer
    brute : brute-force global optimizer

    Notes
    -----
    Simulated annealing is a random algorithm which uses no derivative
    information from the function being optimized. In practice it has
    been more useful in discrete optimization than continuous
    optimization, as there are usually better algorithms for continuous
    optimization problems.

    Some experimentation by trying the different temperature
    schedules and altering their parameters is likely required to
    obtain good performance.

    The randomness in the algorithm comes from random sampling in numpy.
    To obtain the same results you can call `numpy.random.seed` with the
    same seed immediately before calling `anneal`.

    We give a brief description of how the three temperature schedules
    generate new points and vary their temperature.  Temperatures are
    only updated with iterations in the outer loop.  The inner loop is
    over loop over ``xrange(dwell)``, and new points are generated for
    every iteration in the inner loop.  Whether the proposed new points
    are accepted is probabilistic.

    For readability, let ``d`` denote the dimension of the inputs to func.
    Also, let ``x_old`` denote the previous state, and ``k`` denote the
    iteration number of the outer loop.  All other variables not
    defined below are input variables to `anneal` itself.

    In the 'fast' schedule the updates are::

        u ~ Uniform(0, 1, size = d)
        y = sgn(u - 0.5) * T * ((1 + 1/T)**abs(2*u - 1) - 1.0)

        xc = y * (upper - lower)
        x_new = x_old + xc

        c = n * exp(-n * quench)
        T_new = T0 * exp(-c * k**quench)

    In the 'cauchy' schedule the updates are::

        u ~ Uniform(-pi/2, pi/2, size=d)
        xc = learn_rate * T * tan(u)
        x_new = x_old + xc

        T_new = T0 / (1 + k)

    In the 'boltzmann' schedule the updates are::

        std = minimum(sqrt(T) * ones(d), (upper - lower) / (3*learn_rate))
        y ~ Normal(0, std, size = d)
        x_new = x_old + learn_rate * y

        T_new = T0 / log(1 + k)

    References
    ----------
    [1] P. J. M. van Laarhoven and E. H. L. Aarts, "Simulated Annealing: Theory
        and Applications", Kluwer Academic Publishers, 1987.

    [2] W.H. Press et al., "Numerical Recipies: The Art of Scientific Computing",
        Cambridge U. Press, 1987.

    Examples
    --------
    *Example 1.* We illustrate the use of `anneal` to seek the global minimum
    of a function of two variables that is equal to the sum of a positive-
    definite quadratic and two deep "Gaussian-shaped" craters.  Specifically,
    define the objective function `f` as the sum of three other functions,
    ``f = f1 + f2 + f3``.  We suppose each of these has a signature
    ``(z, *params)``, where ``z = (x, y)``, ``params``, and the functions are
    as defined below.

    >>> params = (2, 3, 7, 8, 9, 10, 44, -1, 2, 26, 1, -2, 0.5)
    >>> def f1(z, *params):
    ...     x, y = z
    ...     a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    ...     return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f)

    >>> def f2(z, *params):
    ...     x, y = z
    ...     a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    ...     return (-g*np.exp(-((x-h)**2 + (y-i)**2) / scale))

    >>> def f3(z, *params):
    ...     x, y = z
    ...     a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    ...     return (-j*np.exp(-((x-k)**2 + (y-l)**2) / scale))

    >>> def f(z, *params):
    ...     x, y = z
    ...     a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    ...     return f1(z, *params) + f2(z, *params) + f3(z, *params)

    >>> x0 = np.array([2., 2.])     # Initial guess.
    >>> from scipy import optimize
    >>> np.random.seed(555)   # Seeded to allow replication.
    >>> res = optimize.anneal(f, x0, args=params, schedule='boltzmann',
                              full_output=True, maxiter=500, lower=-10,
                              upper=10, dwell=250, disp=True)
    Warning: Maximum number of iterations exceeded.
    >>> res[0]  # obtained minimum
    array([-1.03914194,  1.81330654])
    >>> res[1]  # function value at minimum
    -3.3817...

    So this run settled on the point [-1.039, 1.813] with a minimum function
    value of about -3.382.  The final temperature was about 212. The run used
    125301 function evaluations, 501 iterations (including the initial guess as
    a iteration), and accepted 61162 points. The status flag of 3 also
    indicates that `maxiter` was reached.

    This problem's true global minimum lies near the point [-1.057, 1.808]
    and has a value of about -3.409.  So these `anneal` results are pretty
    good and could be used as the starting guess in a local optimizer to
    seek a more exact local minimum.

    *Example 2.* To minimize the same objective function using
    the `minimize` approach, we need to (a) convert the options to an
    "options dictionary" using the keys prescribed for this method,
    (b) call the `minimize` function with the name of the method (which
    in this case is 'Anneal'), and (c) take account of the fact that
    the returned value will be a `Result` object (`i.e.`, a dictionary,
    as defined in `optimize.py`).

    All of the allowable options for 'Anneal' when using the `minimize`
    approach are listed in the ``myopts`` dictionary given below, although
    in practice only the non-default values would be needed.  Some of their
    names differ from those used in the `anneal` approach.  We can proceed
    as follows:

    >>> myopts = {
            'schedule'     : 'boltzmann',   # Non-default value.
            'maxfev'       : None,  # Default, formerly `maxeval`.
            'maxiter'      : 500,   # Non-default value.
            'maxaccept'    : None,  # Default value.
            'ftol'         : 1e-6,  # Default, formerly `feps`.
            'T0'           : None,  # Default value.
            'Tf'           : 1e-12, # Default value.
            'boltzmann'    : 1.0,   # Default value.
            'learn_rate'   : 0.5,   # Default value.
            'quench'       : 1.0,   # Default value.
            'm'            : 1.0,   # Default value.
            'n'            : 1.0,   # Default value.
            'lower'        : -10,   # Non-default value.
            'upper'        : +10,   # Non-default value.
            'dwell'        : 250,   # Non-default value.
            'disp'         : True   # Default value.
            }
    >>> from scipy import optimize
    >>> np.random.seed(777)  # Seeded to allow replication.
    >>> res2 = optimize.minimize(f, x0, args=params, method='Anneal',
                                 options=myopts)
    Warning: Maximum number of iterations exceeded.
    >>> res2
      status: 3
     success: False
      accept: 61742
        nfev: 125301
           T: 214.20624873839623
         fun: -3.4084065576676053
           x: array([-1.05757366,  1.8071427 ])
     message: 'Maximum cooling iterations reached'
     nit: 501

    """

    opts = {'schedule': schedule,
            'T0': T0,
            'Tf': Tf,
            'maxfev': maxeval,
            'maxaccept': maxaccept,
            'maxiter': maxiter,
            'boltzmann': boltzmann,
            'learn_rate': learn_rate,
            'ftol': feps,
            'quench': quench,
            'm': m,
            'n': n,
            'lower': lower,
            'upper': upper,
            'dwell': dwell,
            'disp': disp}

    res = _minimize_anneal(func, x0, args, **opts)

    if full_output:
        return res['x'], res['fun'], res['T'], res['nfev'], res['nit'], \
            res['accept'], res['status']
    else:
        return res['x'], res['status']
