    def _has_valid_type(self, key, axis):
        ax = self.obj._get_axis(axis)

        # valid for a label where all labels are in the index
        # slice of lables (where start-end in labels)
        # slice of integers (only if in the lables)
        # boolean

        if isinstance(key, slice):
            return True

        elif is_bool_indexer(key):
            return True

        elif is_list_like_indexer(key):

            # mi is just a passthru
            if isinstance(key, tuple) and isinstance(ax, MultiIndex):
                return True

            # TODO: don't check the entire key unless necessary
            if len(key) and np.all(ax.get_indexer_for(key) < 0):

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
