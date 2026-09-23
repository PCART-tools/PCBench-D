    @Substitution(name='groupby')
    def apply(self, func, *args, **kwargs):
        """
        Apply function and combine results together in an intelligent way.

        The split-apply-combine combination rules attempt to be as common
        sense based as possible. For example:

        case 1:
        group DataFrame
        apply aggregation function (f(chunk) -> Series)
        yield DataFrame, with group axis having group labels

        case 2:
        group DataFrame
        apply transform function ((f(chunk) -> DataFrame with same indexes)
        yield DataFrame with resulting chunks glued together

        case 3:
        group Series
        apply function with f(chunk) -> DataFrame
        yield DataFrame with result of chunks glued together

        Parameters
        ----------
        func : function

        Notes
        -----
        See online documentation for full exposition on how to use apply.

        In the current implementation apply calls func twice on the
        first group to decide whether it can take a fast or slow code
        path. This can lead to unexpected behavior if func has
        side-effects, as they will take effect twice for the first
        group.


        See also
        --------
        pipe : Apply function to the full GroupBy object instead of to each
            group.
        aggregate, transform
        """

        func = self._is_builtin_func(func)

        # this is needed so we don't try and wrap strings. If we could
        # resolve functions to their callable functions prior, this
        # wouldn't be needed
        if args or kwargs:
            if callable(func):

                @wraps(func)
                def f(g):
                    with np.errstate(all='ignore'):
                        return func(g, *args, **kwargs)
            else:
                raise ValueError('func must be a callable if args or '
                                 'kwargs are supplied')
        else:
            f = func

        # ignore SettingWithCopy here in case the user mutates
        with option_context('mode.chained_assignment', None):
            return self._python_apply_general(f)
