    def _pos_idxs(
        self, idxs: np.ndarray[Any, Any] | pli.Series, dim: int
    ) -> pli.Series:
        # pl.UInt32 (polars) or pl.UInt64 (polars_u64_idx).
        idx_type = get_idx_type()

        if isinstance(idxs, pli.Series):
            if idxs.dtype == idx_type:
                return idxs
            if idxs.dtype in {
                UInt8,
                UInt16,
                UInt64 if idx_type == UInt32 else UInt32,
                Int8,
                Int16,
                Int32,
                Int64,
            }:
                if idx_type == UInt32:
                    if idxs.dtype in {Int64, UInt64}:
                        if idxs.max() >= 2**32:  # type: ignore[operator]
                            raise ValueError(
                                "Index positions should be smaller than 2^32."
                            )
                    if idxs.dtype == Int64:
                        if idxs.min() < -(2**32):  # type: ignore[operator]
                            raise ValueError(
                                "Index positions should be bigger than -2^32 + 1."
                            )
                if idxs.dtype in {Int8, Int16, Int32, Int64}:
                    if idxs.min() < 0:  # type: ignore[operator]
                        if idx_type == UInt32:
                            if idxs.dtype in {Int8, Int16}:
                                idxs = idxs.cast(Int32)
                        else:
                            if idxs.dtype in {Int8, Int16, Int32}:
                                idxs = idxs.cast(Int64)

                        idxs = pli.select(
                            pli.when(pli.lit(idxs) < 0)
                            .then(self.shape[dim] + pli.lit(idxs))
                            .otherwise(pli.lit(idxs))
                        ).to_series()

                return idxs.cast(idx_type)

        if _check_for_numpy(idxs) and isinstance(idxs, np.ndarray):
            if idxs.ndim != 1:
                raise ValueError("Only 1D numpy array is supported as index.")
            if idxs.dtype.kind in ("i", "u"):
                # Numpy array with signed or unsigned integers.

                if idx_type == UInt32:
                    if idxs.dtype in {np.int64, np.uint64} and idxs.max() >= 2**32:
                        raise ValueError("Index positions should be smaller than 2^32.")
                    if idxs.dtype == np.int64 and idxs.min() < -(2**32):
                        raise ValueError(
                            "Index positions should be bigger than -2^32 + 1."
                        )
                if idxs.dtype.kind == "i" and idxs.min() < 0:
                    if idx_type == UInt32:
                        if idxs.dtype in (np.int8, np.int16):
                            idxs = idxs.astype(np.int32)
                    else:
                        if idxs.dtype in (np.int8, np.int16, np.int32):
                            idxs = idxs.astype(np.int64)

                    # Update negative indexes to absolute indexes.
                    idxs = np.where(idxs < 0, self.shape[dim] + idxs, idxs)

                return pli.Series("", idxs, dtype=idx_type)

        raise NotImplementedError("Unsupported idxs datatype.")
