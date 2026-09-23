    def _get_common_dtype(self, dtypes: List[DtypeObj]) -> Optional[DtypeObj]:
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
            [t.numpy_dtype if isinstance(t, BaseMaskedDtype) else t for t in dtypes], []
        )
        if np.issubdtype(np_dtype, np.integer):
            return _dtypes[str(np_dtype)]
        return None
