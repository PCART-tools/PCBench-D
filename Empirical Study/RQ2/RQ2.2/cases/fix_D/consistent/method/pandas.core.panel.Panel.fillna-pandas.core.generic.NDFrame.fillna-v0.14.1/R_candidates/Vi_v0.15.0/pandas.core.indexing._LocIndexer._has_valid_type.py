    def _has_valid_type(self, key, axis):
        ax = self.obj._get_axis(axis)

        # valid for a label where all labels are in the index
        # slice of lables (where start-end in labels)
        # slice of integers (only if in the lables)
        # boolean

        if isinstance(key, slice):

            if ax.is_floating():

                # allowing keys to be slicers with no fallback
                pass

            else:
                if key.start is not None:
                    if key.start not in ax:
                        raise KeyError(
                            "start bound [%s] is not the [%s]" %
                            (key.start, self.obj._get_axis_name(axis))
                        )
                if key.stop is not None:
                    if key.stop not in ax:
                        raise KeyError(
                            "stop bound [%s] is not in the [%s]" %
                            (key.stop, self.obj._get_axis_name(axis))
                        )

        elif com._is_bool_indexer(key):
            return True

        elif _is_list_like(key):

            # mi is just a passthru
            if isinstance(key, tuple) and isinstance(ax, MultiIndex):
                return True

            # require at least 1 element in the index
            idx = _ensure_index(key)
            if len(idx) and not idx.isin(ax).any():

                raise KeyError("None of [%s] are in the [%s]" %
                               (key, self.obj._get_axis_name(axis)))

            return True

        else:

            def error():
                if isnull(key):
                    raise ValueError(
                        "cannot use label indexing with a null key")
                raise KeyError("the label [%s] is not in the [%s]" %
                               (key, self.obj._get_axis_name(axis)))

            try:
                key = self._convert_scalar_indexer(key, axis)
                if not key in ax:
                    error()
            except (TypeError) as e:

                # python 3 type errors should be raised
                if 'unorderable' in str(e):  # pragma: no cover
                    error()
                raise
            except:
                error()

        return True
