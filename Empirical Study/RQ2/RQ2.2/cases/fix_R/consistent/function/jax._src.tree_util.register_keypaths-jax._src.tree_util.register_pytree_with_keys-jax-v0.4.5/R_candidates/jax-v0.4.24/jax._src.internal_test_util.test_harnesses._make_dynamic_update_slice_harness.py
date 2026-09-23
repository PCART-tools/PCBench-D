def _make_dynamic_update_slice_harness(name,
                                       shape=(3,),
                                       start_indices=(1,),
                                       dtype=np.float32,
                                       update_shape=(1,)):
  for enable_xla in [False, True]:
    define(
        lax.dynamic_update_slice_p,
        (
            f"{name}_operand={jtu.format_shape_dtype_string(shape, dtype)}"  # type: ignore
            f"_update={jtu.format_shape_dtype_string(update_shape, dtype)}"
            f"_{start_indices=}_{enable_xla=}"),
        lax.dynamic_update_slice,
        [
            RandArg(shape, dtype),  # type: ignore
            RandArg(update_shape, dtype),  # type: ignore
            np.array(start_indices)
        ],  # type: ignore
        dtype=dtype,
        shape=shape,  # type: ignore
        start_indices=start_indices,  # type: ignore
        update_shape=update_shape,  # type: ignore
        enable_xla=enable_xla)
