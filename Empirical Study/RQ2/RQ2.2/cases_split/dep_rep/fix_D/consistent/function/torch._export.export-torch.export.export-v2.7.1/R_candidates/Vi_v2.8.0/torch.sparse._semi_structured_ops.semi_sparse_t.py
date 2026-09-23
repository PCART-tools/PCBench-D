def semi_sparse_t(func, types, args=(), kwargs=None) -> torch.Tensor:
    assert len(args) == 1
    self = args[0]
    assert isinstance(self, torch.sparse.SparseSemiStructuredTensor)
    assert len(self.shape) == 2
    # Because we cannot go from the compressed representation back to the dense representation currently,
    # we just keep track of how many times we have been transposed. Depending on whether the sparse matrix
    # is the first or second argument, we expect an even / odd number of calls to transpose respectively.
    return self.__class__(
        torch.Size([self.shape[-1], self.shape[0]]),
        packed=self.packed_t,
        meta=self.meta_t,
        packed_t=self.packed,
        meta_t=self.meta,
        compressed_swizzled_bitmask=(
            self.compressed_swizzled_bitmask.transpose(0, 1)
            if self.compressed_swizzled_bitmask is not None
            else None
        ),
        fuse_transpose_cusparselt=args[0].fuse_transpose_cusparselt,
        alg_id_cusparselt=args[0].alg_id_cusparselt,
    )
