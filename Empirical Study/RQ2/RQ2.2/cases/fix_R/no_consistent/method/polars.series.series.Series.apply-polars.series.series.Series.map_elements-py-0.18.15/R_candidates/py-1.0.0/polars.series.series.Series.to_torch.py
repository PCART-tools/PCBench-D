    @unstable()
    def to_torch(self) -> torch.Tensor:
        """
        Convert this Series to a PyTorch Tensor.

        .. versionadded:: 0.20.23

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Notes
        -----
        PyTorch tensors do not support UInt16, UInt32, or UInt64; these dtypes
        will be automatically cast to Int32, Int64, and Int64, respectively.

        Examples
        --------
        >>> s = pl.Series("x", [1, 0, 1, 2, 0], dtype=pl.UInt8)
        >>> s.to_torch()
        tensor([1, 0, 1, 2, 0], dtype=torch.uint8)
        >>> s = pl.Series("x", [5.5, -10.0, 2.5], dtype=pl.Float32)
        >>> s.to_torch()
        tensor([  5.5000, -10.0000,   2.5000])
        """
        torch = import_optional("torch")

        # PyTorch tensors do not support uint16/32/64
        if self.dtype in (UInt32, UInt64):
            srs = self.cast(Int64)
        elif self.dtype == UInt16:
            srs = self.cast(Int32)
        else:
            srs = self

        # we have to build the tensor from a writable array or PyTorch will complain
        # about it (as writing to readonly array results in undefined behavior)
        numpy_array = srs.to_numpy(writable=True)
        tensor = torch.from_numpy(numpy_array)

        # note: named tensors are currently experimental
        # tensor.rename(self.name)
        return tensor
