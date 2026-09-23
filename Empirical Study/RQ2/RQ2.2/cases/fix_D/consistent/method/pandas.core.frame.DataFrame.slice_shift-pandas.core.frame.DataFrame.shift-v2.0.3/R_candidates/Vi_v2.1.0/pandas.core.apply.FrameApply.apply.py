    def apply(self) -> DataFrame | Series:
        """compute the results"""
        # dispatch to handle list-like or dict-like
        if is_list_like(self.func):
            return self.apply_list_or_dict_like()

        # all empty
        if len(self.columns) == 0 and len(self.index) == 0:
            return self.apply_empty_result()

        # string dispatch
        if isinstance(self.func, str):
            return self.apply_str()

        # ufunc
        elif isinstance(self.func, np.ufunc):
            with np.errstate(all="ignore"):
                results = self.obj._mgr.apply("apply", func=self.func)
            # _constructor will retain self.index and self.columns
            return self.obj._constructor_from_mgr(results, axes=results.axes)

        # broadcasting
        if self.result_type == "broadcast":
            return self.apply_broadcast(self.obj)

        # one axis empty
        elif not all(self.obj.shape):
            return self.apply_empty_result()

        # raw
        elif self.raw:
            return self.apply_raw()

        return self.apply_standard()
