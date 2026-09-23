def _make_dynamic_slice_harness(name,
                                shape=(3,),
                                start_indices=(1,),
                                limit_indices=(2,),
                                dtype=np.float32):
  for enable_xla in [False, True]:
    define(
        lax.dynamic_slice_p,
        f"{name}_a={jtu.format_shape_dtype_string(shape, dtype)}_{start_indices=}_{limit_indices=}_enablexla={enable_xla}",
        # type: ignore
        lax.dynamic_slice,
        [
            RandArg(shape, dtype),  # type: ignore
            np.array(list(start_indices)),
            StaticArg(tuple(map(operator.sub, limit_indices, start_indices)))
        ],  # type: ignore
        dtype=dtype,
        shape=shape,  # type: ignore
        start_indices=start_indices,  # type: ignore
        limit_indices=limit_indices,  # type: ignore
        enable_xla=enable_xla)
