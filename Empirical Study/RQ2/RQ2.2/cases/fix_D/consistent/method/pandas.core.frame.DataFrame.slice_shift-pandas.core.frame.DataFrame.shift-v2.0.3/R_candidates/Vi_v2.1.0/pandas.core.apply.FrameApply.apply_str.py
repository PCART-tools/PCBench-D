    def apply_str(self) -> DataFrame | Series:
        # Caller is responsible for checking isinstance(self.func, str)
        # TODO: GH#39993 - Avoid special-casing by replacing with lambda
        if self.func == "size":
            # Special-cased because DataFrame.size returns a single scalar
            obj = self.obj
            value = obj.shape[self.axis]
            return obj._constructor_sliced(value, index=self.agg_axis)
        return super().apply_str()
