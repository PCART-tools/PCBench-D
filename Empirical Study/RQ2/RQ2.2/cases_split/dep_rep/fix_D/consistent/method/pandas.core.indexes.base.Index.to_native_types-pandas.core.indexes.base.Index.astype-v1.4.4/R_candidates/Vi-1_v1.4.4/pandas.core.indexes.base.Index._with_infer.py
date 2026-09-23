    @classmethod
    def _with_infer(cls, *args, **kwargs):
        """
        Constructor that uses the 1.0.x behavior inferring numeric dtypes
        for ndarray[object] inputs.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", ".*the Index constructor", FutureWarning)
            result = cls(*args, **kwargs)

        if result.dtype == _dtype_obj and not result._is_multi:
            # error: Argument 1 to "maybe_convert_objects" has incompatible type
            # "Union[ExtensionArray, ndarray[Any, Any]]"; expected
            # "ndarray[Any, Any]"
            values = lib.maybe_convert_objects(result._values)  # type: ignore[arg-type]
            if values.dtype.kind in ["i", "u", "f"]:
                return Index(values, name=result.name)

        return result
