  def __getitem__(self, idx):
    from jax._src.lax import lax
    from jax._src.numpy import lax_numpy
    self._check_if_deleted()

    if isinstance(self.sharding, PmapSharding):
      if config.pmap_no_rank_reduction.value:
        cidx = idx if isinstance(idx, tuple) else (idx,)

        padded_cidx = tuple(
            slice(i, i + 1, None) if isinstance(i, int) else i for i in cidx
        ) + (slice(None),) * (len(self.shape) - len(cidx))
      else:
        if not isinstance(idx, tuple):
          padded_cidx = (idx,) + (slice(None),) * (len(self.shape) - 1)
        else:
          padded_cidx = idx + (slice(None),) * (len(self.shape) - len(idx))

      indices = tuple(self.sharding.devices_indices_map(self.shape).values())
      try:
        arr_idx = indices.index(padded_cidx)
      except ValueError:
        arr_idx = None
      if arr_idx is not None:
        a = self._arrays[arr_idx]
        out = ArrayImpl(
            a.aval, SingleDeviceSharding(_get_device(a)), [a], committed=False,
            _skip_checks=True)

        if config.pmap_no_rank_reduction.value:
          # If cidx was the index of a single shard, then it corresponds to one
          # shard of the chunked dimension.
          dims = tuple(i for i, x in enumerate(cidx) if isinstance(x, int))
          return lax.squeeze(out, dimensions=dims)
        else:
          return out

    return lax_numpy._rewriting_take(self, idx)
