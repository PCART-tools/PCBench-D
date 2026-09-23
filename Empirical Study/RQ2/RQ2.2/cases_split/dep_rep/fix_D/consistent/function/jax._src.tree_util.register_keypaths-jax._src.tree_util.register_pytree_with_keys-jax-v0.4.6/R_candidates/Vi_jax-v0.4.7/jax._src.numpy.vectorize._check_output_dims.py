def _check_output_dims(
    func: Callable,
    dim_sizes: Dict[str, int],
    expected_output_core_dims: List[CoreDims],
    error_context: str = "",
) -> Callable:
  """Check that output core dimensions match the signature."""
  def wrapped(*args):
    out = func(*args)
    out_shapes = map(jnp.shape, out if isinstance(out, tuple) else [out])

    if expected_output_core_dims is None:
      output_core_dims = [()] * len(out_shapes)
    else:
      output_core_dims = expected_output_core_dims
      if len(output_core_dims) > 1 and not isinstance(out, tuple):
        raise TypeError(
            "output must be a tuple when multiple outputs are expected, "
            "got: {!r}\n{}".format(out, error_context))
      if len(out_shapes) != len(output_core_dims):
        raise TypeError(
            'wrong number of output arguments: expected %r, got %r %s'
            % (len(output_core_dims), len(out_shapes), error_context))

    sizes = dict(dim_sizes)
    for shape, core_dims in zip(out_shapes, output_core_dims):
      _update_dim_sizes(sizes, shape, core_dims, error_context,
                        is_input=False)

    return out
  return wrapped
