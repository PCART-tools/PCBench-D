    def _transform_general(self, func, *args, **kwargs):
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
