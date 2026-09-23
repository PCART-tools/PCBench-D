    def _get_common_dtype(self, dtypes: list[DtypeObj]) -> DtypeObj | None:
        # we only handle nullable EA dtypes and numeric numpy dtypes
        if not all(
            isinstance(t, BaseMaskedDtype)
            or (
                isinstance(t, np.dtype)
                and (np.issubdtype(t, np.number) or np.issubdtype(t, np.bool_))
            )
            for t in dtypes
        ):
            return None
        np_dtype = np.find_common_type(
            # error: List comprehension has incompatible type List[Union[Any,
            # dtype, ExtensionDtype]]; expected List[Union[dtype, None, type,
            # _SupportsDtype, str, Tuple[Any, Union[int, Sequence[int]]],
            # List[Any], _DtypeDict, Tuple[Any, Any]]]
            [
                t.numpy_dtype  # type: ignore[misc]
                if isinstance(t, BaseMaskedDtype)
                else t
                for t in dtypes
            ],
            [],
        )
        if np.issubdtype(np_dtype, np.integer):
            return INT_STR_TO_DTYPE[str(np_dtype)]
        elif np.issubdtype(np_dtype, np.floating):
            from pandas.core.arrays.floating import FLOAT_STR_TO_DTYPE

            return FLOAT_STR_TO_DTYPE[str(np_dtype)]
        return None
