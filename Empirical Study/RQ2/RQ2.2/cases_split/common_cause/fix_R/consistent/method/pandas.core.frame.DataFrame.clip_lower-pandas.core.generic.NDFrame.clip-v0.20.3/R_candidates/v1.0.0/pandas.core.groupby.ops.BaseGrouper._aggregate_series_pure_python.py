    def _aggregate_series_pure_python(self, obj: Series, func):

        group_index, _, ngroups = self.group_info

        counts = np.zeros(ngroups, dtype=int)
        result = None

        splitter = get_splitter(obj, group_index, ngroups, axis=0)

        for label, group in splitter:
            res = func(group)
            if result is None:
                if isinstance(res, (Series, Index, np.ndarray)):
                    if len(res) == 1:
                        # e.g. test_agg_lambda_with_timezone lambda e: e.head(1)
                        # FIXME: are we potentially losing import res.index info?
                        res = res.item()
                    else:
                        raise ValueError("Function does not reduce")
                result = np.empty(ngroups, dtype="O")

            counts[label] = group.shape[0]
            result[label] = res

        assert result is not None
        result = lib.maybe_convert_objects(result, try_float=0)
        # TODO: try_cast back to EA?

        return result, counts
