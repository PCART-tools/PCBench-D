def _match_annot(axis_name: core.AxisName, axis_size: int, val: Any,
                 shard_axis_src: Dict[core.AxisName, int],
                 dst_annotation: Optional[int]
                 ) -> Tuple[Any, Dict[core.AxisName, int]]:
  shard_axis_out = dict(shard_axis_src)
  src = shard_axis_out.pop(axis_name, None)
  dst = _annot_to_flat(np.ndim(val) + (src is None), shard_axis_out.values(),
                       dst_annotation)
  with core.eval_context():
    if src == dst:
      outval = val
    elif type(src) == type(dst) == int:
      outval = batching.moveaxis(val, src, dst)
      shard_axis_out = _moveaxis(np.ndim(val), shard_axis_src, src, dst)
    elif src is None and dst is not None:
      outval = batching.broadcast(val, axis_size, dst)
      shard_axis_out = {n: d + (dst <= d) for n, d in shard_axis_out.items()}
    else:
      raise NotImplementedError
  return outval, shard_axis_out
