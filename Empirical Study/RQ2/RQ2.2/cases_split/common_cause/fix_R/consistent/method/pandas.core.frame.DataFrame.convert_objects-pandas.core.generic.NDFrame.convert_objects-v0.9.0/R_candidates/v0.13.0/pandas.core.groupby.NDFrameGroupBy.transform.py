    def transform(self, func, *args, **kwargs):
        """
        Call function producing a like-indexed DataFrame on each group and
        return a DataFrame having the same indexes as the original object
        filled with the transformed values

        Parameters
        ----------
        f : function
            Function to apply to each subframe

        Notes
        -----
        Each subframe is endowed the attribute 'name' in case you need to know
        which group you are working on.

        Examples
        --------
        >>> grouped = df.groupby(lambda x: mapping[x])
        >>> grouped.transform(lambda x: (x - x.mean()) / x.std())
        """
        from pandas.tools.merge import concat

        applied = []

        obj = self._obj_with_exclusions
        gen = self.grouper.get_iterator(obj, axis=self.axis)
        fast_path, slow_path = self._define_paths(func, *args, **kwargs)

        path = None
        for name, group in gen:
            object.__setattr__(group, 'name', name)

            if path is None:
                # Try slow path and fast path.
                try:
                    path, res = self._choose_path(fast_path, slow_path, group)
                except TypeError:
                    return self._transform_item_by_item(obj, fast_path)
                except Exception:  # pragma: no cover
                    res = fast_path(group)
                    path = fast_path
            else:
                res = path(group)

            # broadcasting
            if isinstance(res, Series):
                if res.index.is_(obj.index):
                    group.T.values[:] = res
                else:
                    group.values[:] = res

                applied.append(group)
            else:
                applied.append(res)

        concat_index = obj.columns if self.axis == 0 else obj.index
        concatenated = concat(applied, join_axes=[concat_index],
                              axis=self.axis, verify_integrity=False)
        concatenated.sort_index(inplace=True)
        return concatenated
