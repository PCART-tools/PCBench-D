    def _pos_idxs(self, size: int) -> Series:
        # Unsigned or signed Series (ordered from fastest to slowest).
        #   - pl.UInt32 (polars) or pl.UInt64 (polars_u64_idx) Series indexes.
        #   - Other unsigned Series indexes are converted to pl.UInt32 (polars)
        #     or pl.UInt64 (polars_u64_idx).
        #   - Signed Series indexes are converted pl.UInt32 (polars) or
        #     pl.UInt64 (polars_u64_idx) after negative indexes are converted
        #     to absolute indexes.

        # pl.UInt32 (polars) or pl.UInt64 (polars_u64_idx).
        idx_type = get_index_type()

        if self.dtype == idx_type:
            return self

        if not self.dtype.is_integer():
            msg = "unsupported idxs datatype"
            raise NotImplementedError(msg)

        if self.len() == 0:
            return Series(self.name, [], dtype=idx_type)

        if idx_type == UInt32:
            if self.dtype in {Int64, UInt64}:
                if self.max() >= 2**32:  # type: ignore[operator]
                    msg = "index positions should be smaller than 2^32"
                    raise ValueError(msg)
            if self.dtype == Int64:
                if self.min() < -(2**32):  # type: ignore[operator]
                    msg = "index positions should be bigger than -2^32 + 1"
                    raise ValueError(msg)

        if self.dtype.is_signed_integer():
            if self.min() < 0:  # type: ignore[operator]
                if idx_type == UInt32:
                    idxs = self.cast(Int32) if self.dtype in {Int8, Int16} else self
                else:
                    idxs = (
                        self.cast(Int64) if self.dtype in {Int8, Int16, Int32} else self
                    )

                # Update negative indexes to absolute indexes.
                return (
                    idxs.to_frame()
                    .select(
                        F.when(F.col(idxs.name) < 0)
                        .then(size + F.col(idxs.name))
                        .otherwise(F.col(idxs.name))
                        .cast(idx_type)
                    )
                    .to_series(0)
                )

        return self.cast(idx_type)
