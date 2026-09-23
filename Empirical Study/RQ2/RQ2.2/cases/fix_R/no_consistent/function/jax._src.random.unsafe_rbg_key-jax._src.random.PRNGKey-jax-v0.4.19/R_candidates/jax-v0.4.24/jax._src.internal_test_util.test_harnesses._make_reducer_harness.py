def _make_reducer_harness(prim,
                          name,
                          *,
                          shape=(2, 3),
                          axes=(0,),
                          dtype=np.int32):
  define(
      prim,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}",
      lambda arg: prim.bind(arg, axes=axes), [RandArg(shape, dtype)],
      prim=prim,
      shape=shape,
      dtype=dtype,
      axes=axes)
