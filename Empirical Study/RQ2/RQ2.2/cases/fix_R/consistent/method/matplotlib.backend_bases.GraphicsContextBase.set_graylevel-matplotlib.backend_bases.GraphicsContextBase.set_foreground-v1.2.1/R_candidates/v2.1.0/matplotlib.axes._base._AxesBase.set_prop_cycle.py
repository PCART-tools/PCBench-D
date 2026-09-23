    def set_prop_cycle(self, *args, **kwargs):
        """
        Set the property cycle for any future plot commands on this Axes.

        set_prop_cycle(arg)
        set_prop_cycle(label, itr)
        set_prop_cycle(label1=itr1[, label2=itr2[, ...]])

        Form 1 simply sets given `Cycler` object.

        Form 2 creates and sets  a `Cycler` from a label and an iterable.

        Form 3 composes and sets  a `Cycler` as an inner product of the
        pairs of keyword arguments. In other words, all of the
        iterables are cycled simultaneously, as if through zip().

        Parameters
        ----------
        arg : Cycler
            Set the given Cycler.
            Can also be `None` to reset to the cycle defined by the
            current style.

        label : str
            The property key. Must be a valid `Artist` property.
            For example, 'color' or 'linestyle'. Aliases are allowed,
            such as 'c' for 'color' and 'lw' for 'linewidth'.

        itr : iterable
            Finite-length iterable of the property values. These values
            are validated and will raise a ValueError if invalid.

        See Also
        --------
            :func:`cycler`      Convenience function for creating your
                                own cyclers.

        """
        if args and kwargs:
            raise TypeError("Cannot supply both positional and keyword "
                            "arguments to this method.")
        if len(args) == 1 and args[0] is None:
            prop_cycle = None
        else:
            prop_cycle = cycler(*args, **kwargs)
        self._get_lines.set_prop_cycle(prop_cycle)
        self._get_patches_for_fill.set_prop_cycle(prop_cycle)
