  def process_call(self, call_primitive, f, tracers, params):
    assert call_primitive.multiple_results
    params = dict(params, name=params.get('name', f.__name__))
    vals, dims = unzip2((t.val, t.batch_dim) for t in tracers)
    if all(bdim is not_mapped for bdim in dims):
      return call_primitive.bind(f, *vals, **params)
    sizes = (x.shape[d] if type(d) is int else len(d.segment_lengths)
             for x, d in zip(vals, dims) if d is not not_mapped)
    axis_size, = core.dedup_referents(sizes)
    segment_lens, dims = indirectify_ragged_axes(dims)
    f_, dims_out = batch_subtrace(f, self.main, tuple(dims))
    f_ = _update_annotation(
        f_, f.in_type, axis_size, self.axis_name, dims, segment_lens)
    vals_out = call_primitive.bind(f_, *segment_lens, *vals, **params)
    vals_out, dims_out = resolve_ragged_axes(vals_out, dims_out())
    src = source_info_util.current()
    return [BatchTracer(self, v, d, src) for v, d in zip(vals_out, dims_out)]
