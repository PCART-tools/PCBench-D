    def _format_native_types(
        self, *, na_rep: str = "NaN", quoting=None, **kwargs
    ) -> npt.NDArray[np.object_]:
        # GH 28210: use base method but with different default na_rep
        return super()._format_native_types(na_rep=na_rep, quoting=quoting, **kwargs)
