    def __init__(self, function, inverse, bounded_0_1=True, check_params=None):
        """
        Parameters
        ----------

        function : callable
            A callable implementing the function receiving the variable as
            first argument and any additional parameters in a list as second
            argument.
        inverse : callable
            A callable implementing the inverse function receiving the variable
            as first argument and any additional parameters in a list as
            second argument. It must satisfy 'inverse(function(x, p), p) == x'.
        bounded_0_1: bool or callable
            A boolean indicating whether the function is bounded in the [0,1]
            interval, or a callable taking a list of values for the additional
            parameters, and returning a boolean indicating whether the function
            is bounded in the [0,1] interval for that combination of
            parameters. Default True.
        check_params: callable or None
            A callable taking a list of values for the additional parameters
            and returning a boolean indicating whether that combination of
            parameters is valid. It is only required if the function has
            additional parameters and some of them are restricted.
            Default None.

        """

        self.function = function
        self.inverse = inverse

        if callable(bounded_0_1):
            self._bounded_0_1 = bounded_0_1
        else:
            self._bounded_0_1 = lambda x: bounded_0_1

        if check_params is None:
            self._check_params = lambda x: True
        elif callable(check_params):
            self._check_params = check_params
        else:
            raise ValueError("Invalid 'check_params' argument.")
