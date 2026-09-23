    def transform_dict_like(self, func):
        """
        Compute transform in the case of a dict-like func
        """
        from pandas.core.reshape.concat import concat

        obj = self.obj
        args = self.args
        kwargs = self.kwargs

        # transform is currently only for Series/DataFrame
        assert isinstance(obj, ABCNDFrame)

        if len(func) == 0:
            raise ValueError("No transform functions were provided")

        func = self.normalize_dictlike_arg("transform", obj, func)

        results: dict[Hashable, DataFrame | Series] = {}
        failed_names = []
        all_type_errors = True
        for name, how in func.items():
            colg = obj._gotitem(name, ndim=1)
            try:
                results[name] = colg.transform(how, 0, *args, **kwargs)
            except Exception as err:
                if str(err) in {
                    "Function did not transform",
                    "No transform functions were provided",
                }:
                    raise err
                else:
                    if not isinstance(err, TypeError):
                        all_type_errors = False
                    failed_names.append(name)
        # combine results
        if not results:
            klass = TypeError if all_type_errors else ValueError
            raise klass("Transform function failed")
        if len(failed_names) > 0:
            warnings.warn(
                f"{failed_names} did not transform successfully. If any error is "
                f"raised, this will raise in a future version of pandas. "
                f"Drop these columns/ops to avoid this warning.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
        return concat(results, axis=1)
