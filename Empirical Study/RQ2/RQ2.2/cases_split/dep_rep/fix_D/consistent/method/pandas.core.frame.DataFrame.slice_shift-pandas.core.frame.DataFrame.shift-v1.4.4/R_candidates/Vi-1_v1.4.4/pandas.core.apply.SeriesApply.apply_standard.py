    def apply_standard(self) -> DataFrame | Series:
        f = self.f
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
                # error: Argument 2 to "map_infer" has incompatible type
                # "Union[Callable[..., Any], str, List[Union[Callable[..., Any], str]],
                # Dict[Hashable, Union[Union[Callable[..., Any], str],
                # List[Union[Callable[..., Any], str]]]]]"; expected
                # "Callable[[Any], Any]"
                mapped = lib.map_infer(
                    values,
                    f,  # type: ignore[arg-type]
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
