    def apply_standard(self) -> DataFrame | Series:
        # caller is responsible for ensuring that f is Callable
        f = cast(Callable, self.f)
        obj = self.obj

        with np.errstate(all="ignore"):
            if isinstance(f, np.ufunc):
                return f(obj)

            # row-wise access
            if is_extension_array_dtype(obj.dtype) and hasattr(obj._values, "map"):
                # GH#23179 some EAs do not have `map`
                mapped = obj._values.map(f)
            else:
                values = obj.astype(object)._values
                mapped = lib.map_infer(
                    values,
                    f,
                    convert=self.convert_dtype,
                )

        if len(mapped) and isinstance(mapped[0], ABCSeries):
            # GH#43986 Need to do list(mapped) in order to get treated as nested
            #  See also GH#25959 regarding EA support
            return obj._constructor_expanddim(list(mapped), index=obj.index)
        else:
            return obj._constructor(mapped, index=obj.index).__finalize__(
                obj, method="apply"
            )
