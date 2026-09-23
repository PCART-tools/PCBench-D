    def filter(self, func, dropna=True, *args, **kwargs):  # noqa
        """
        Return a copy of a DataFrame excluding elements from groups that
        do not satisfy the boolean criterion specified by func.

        Parameters
        ----------
        f : function
            Function to apply to each subframe. Should return True or False.
        dropna : Drop groups that do not pass the filter. True by default;
            if False, groups that evaluate False are filled with NaNs.

        Notes
        -----
        Each subframe is endowed the attribute 'name' in case you need to know
        which group you are working on.

        Examples
        --------
        >>> grouped = df.groupby(lambda x: mapping[x])
        >>> grouped.filter(lambda x: x['A'].sum() + x['B'].sum() > 0)
        """

        indices = []

        obj = self._selected_obj
        gen = self.grouper.get_iterator(obj, axis=self.axis)

        for name, group in gen:
            object.__setattr__(group, 'name', name)

            res = func(group, *args, **kwargs)

            try:
                res = res.squeeze()
            except AttributeError:  # allow e.g., scalars and frames to pass
                pass

            # interpret the result of the filter
            if is_bool(res) or (is_scalar(res) and isnull(res)):
                if res and notnull(res):
                    indices.append(self._get_index(name))
            else:
                # non scalars aren't allowed
                raise TypeError("filter function returned a %s, "
                                "but expected a scalar bool" %
                                type(res).__name__)

        return self._apply_filter(indices, dropna)
