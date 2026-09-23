def _scale_and_translate(x, output_shape: core.Shape,
                         spatial_dims: Sequence[int], scale, translation,
                         kernel, antialias: bool, precision):
  input_shape = x.shape
  assert len(input_shape) == len(output_shape)
  assert len(spatial_dims) == len(scale)
  assert len(spatial_dims) == len(translation)
  if len(spatial_dims) == 0:
    return x
  contractions = []
  in_indices = list(range(len(output_shape)))
  out_indices = list(range(len(output_shape)))
  for i, d in enumerate(spatial_dims):
    d = canonicalize_axis(d, x.ndim)
    m = input_shape[d]
    n = output_shape[d]
    w = compute_weight_mat(m, n, scale[i], translation[i],
                           kernel, antialias).astype(x.dtype)
    contractions.append(w)
    contractions.append([d, len(output_shape) + i])
    out_indices[d] = len(output_shape) + i
  contractions.append(out_indices)
  return jnp.einsum(x, in_indices, *contractions, precision=precision)
