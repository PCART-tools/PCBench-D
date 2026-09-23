@partial(jit, static_argnums=(1, 2, 3, 4))
def _resize(image, shape: core.Shape, method: Union[str, ResizeMethod],
            antialias: bool, precision):
  if len(shape) != image.ndim:
    msg = ('shape must have length equal to the number of dimensions of x; '
           f' {shape} vs {image.shape}')
    raise ValueError(msg)
  if isinstance(method, str):
    method = ResizeMethod.from_string(method)
  if method == ResizeMethod.NEAREST:
    return _resize_nearest(image, shape)
  assert isinstance(method, ResizeMethod)
  kernel = _kernels[method]

  image, = promote_dtypes_inexact(image)
  # Skip dimensions that have scale=1 and translation=0, this is only possible
  # since all of the current resize methods (kernels) are interpolating, so the
  # output = input under an identity warp.
  spatial_dims = tuple(i for i in range(len(shape))
                       if not core.definitely_equal(image.shape[i], shape[i]))
  scale = [1.0 if core.definitely_equal(shape[d], 0) else core.dimension_as_value(shape[d]) / core.dimension_as_value(image.shape[d])
           for d in spatial_dims]
  return _scale_and_translate(image, shape, spatial_dims,
                              scale, [0.] * len(spatial_dims), kernel,
                              antialias, precision)
