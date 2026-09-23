    def apply_standard(self):

        # try to reduce first (by default)
        # this only matters if the reduction in values is of different dtype
        # e.g. if we want to apply to a SparseFrame, then can't directly reduce

        # we cannot reduce using non-numpy dtypes,
        # as demonstrated in gh-12244
        if (
            self.result_type in ["reduce", None]
            and not self.dtypes.apply(is_extension_array_dtype).any()
            # Disallow complex_internals since libreduction shortcut raises a TypeError
            and not self.agg_axis._has_complex_internals
        ):

            values = self.values
            index = self.obj._get_axis(self.axis)
            labels = self.agg_axis
            empty_arr = np.empty(len(index), dtype=values.dtype)

            # Preserve subclass for e.g. test_subclassed_apply
            dummy = self.obj._constructor_sliced(
                empty_arr, index=index, dtype=values.dtype
            )

            try:
                result = libreduction.compute_reduction(
                    values, self.f, axis=self.axis, dummy=dummy, labels=labels
                )
            except ValueError as err:
                if "Function does not reduce" not in str(err):
                    # catch only ValueError raised intentionally in libreduction
                    raise
            except TypeError:
                # e.g. test_apply_ignore_failures we just ignore
                if not self.ignore_failures:
                    raise
            except ZeroDivisionError:
                # reached via numexpr; fall back to python implementation
                pass
            else:
                return self.obj._constructor_sliced(result, index=labels)

        # compute the result using the series generator
        results, res_index = self.apply_series_generator()

        # wrap results
        return self.wrap_results(results, res_index)
