    def _aggregate_multiple_funcs(self, arg, *args, **kwargs) -> DataFrame:
        if isinstance(arg, dict):
            if self.as_index:
                # GH 15931
                raise SpecificationError("nested renamer is not supported")
            else:
                # GH#50684 - This accidentally worked in 1.x
                arg = list(arg.items())
        elif any(isinstance(x, (tuple, list)) for x in arg):
            arg = [(x, x) if not isinstance(x, (tuple, list)) else x for x in arg]
        else:
            # list of functions / function names
            columns = []
            for f in arg:
                columns.append(com.get_callable_name(f) or f)

            arg = zip(columns, arg)

        results: dict[base.OutputKey, DataFrame | Series] = {}
        with com.temp_setattr(self, "as_index", True):
            # Combine results using the index, need to adjust index after
            # if as_index=False (GH#50724)
            for idx, (name, func) in enumerate(arg):
                key = base.OutputKey(label=name, position=idx)
                results[key] = self.aggregate(func, *args, **kwargs)

        if any(isinstance(x, DataFrame) for x in results.values()):
            from pandas import concat

            res_df = concat(
                results.values(), axis=1, keys=[key.label for key in results]
            )
            return res_df

        indexed_output = {key.position: val for key, val in results.items()}
        output = self.obj._constructor_expanddim(indexed_output, index=None)
        output.columns = Index(key.label for key in results)

        output = self._reindex_output(output)
        return output
