    def filter(self, func, dropna=True, *args, **kwargs):
        """
        Return a copy of a Series excluding elements from groups that
        do not satisfy the boolean criterion specified by func.

        Parameters
        ----------
        func : function
            To apply to each group. Should return True or False.
        dropna : Drop groups that do not pass the filter. True by default;
            if False, groups that evaluate False are filled with NaNs.

        Examples
        --------
        >>> grouped.filter(lambda x: x.mean() > 0)

        Returns
        -------
        filtered : Series
        """
        if isinstance(func, compat.string_types):
            wrapper = lambda x: getattr(x, func)(*args, **kwargs)
        else:
            wrapper = lambda x: func(x, *args, **kwargs)

        # Interpret np.nan as False.
        def true_and_notnull(x, *args, **kwargs):
            b = wrapper(x, *args, **kwargs)
            return b and notnull(b)

        try:
            indices = []
            for name, group in self:
                if true_and_notnull(group) and name in self.indices:
                    indices.append(self.indices[name])

        except ValueError:
            raise TypeError("the filter must return a boolean result")
        except TypeError:
            raise TypeError("the filter must return a boolean result")

        filtered = self._apply_filter(indices, dropna)
        return filtered
