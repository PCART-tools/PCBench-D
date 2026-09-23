    def apply(self) -> DataFrame | Series:
        obj = self.obj

        if len(obj) == 0:
            return self.apply_empty_result()

        # dispatch to agg
        if is_list_like(self.f):
            return self.apply_multiple()

        if isinstance(self.f, str):
            # if we are a string, try to dispatch
            return self.apply_str()

        return self.apply_standard()
