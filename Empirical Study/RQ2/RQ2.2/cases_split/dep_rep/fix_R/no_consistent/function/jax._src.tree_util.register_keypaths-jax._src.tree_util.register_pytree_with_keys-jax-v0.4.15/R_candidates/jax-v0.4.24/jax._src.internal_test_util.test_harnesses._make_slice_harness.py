def _make_slice_harness(name,
                        shape=(3,),
                        start_indices=(1,),
                        limit_indices=(2,),
                        strides=None,
                        dtype=np.float32):
  define(
      lax.slice_p,
      f"{name}_a={jtu.format_shape_dtype_string(shape, dtype)}_{start_indices=}_{limit_indices=}_{strides=}",
      # type: ignore
      lax.slice,
      [
          RandArg(shape, dtype),  # type: ignore
          StaticArg(start_indices),  # type: ignore
          StaticArg(limit_indices),  # type: ignore
          StaticArg(strides)
      ],  # type: ignore
      dtype=dtype,
      shape=shape,  # type: ignore
      start_indices=start_indices,  # type: ignore
      limit_indices=limit_indices)  # type: ignore
