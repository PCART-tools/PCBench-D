def _lower_tpu_kernel(module: ir.Module, hardware_generation: int) -> ir.Module:
  """Runs MLIR passes lowering the given module to an MLIR module.

  Args:
    module: The MLIR module to lower.
    hardware_generation: The TPU hardware generation to target.

  Returns:
    A pair containing an MLIR module implementing the kernel specified by the
    argument and a tuple of additional constant arguments that should be
    appended to the kernel invocation.

  """
  try:
    module.operation.verify()
  except ir.MLIRError as e:
    raise ValueError("The compiled module fails MLIR verification") from e

  with ir.Context() as ctx, ir.Location.unknown():
    tpu.register_dialect(ctx)
    mhlo.register_mhlo_dialect(ctx)
    mhlo.register_mhlo_passes()
    # We'll mutate the module, so clone it.
    module = ir.Module.parse(
        module.operation.get_asm(binary=True, enable_debug_info=True)
    )

    if config.jax_mosaic_allow_hlo:
      # Run hlo dialect conversion: hlo -> linalg -> vector.
      pipeline = [
          "hlo-legalize-to-arithmetic",
          "func.func(hlo-legalize-to-linalg)",
          "func.func(linalg-vectorization)",
      ]
      PassManager.parse(f"builtin.module({','.join(pipeline)})").run(
          module.operation
      )

    infer_memref_layout.infer_module(module, hardware_generation)

    pipeline = [
        "canonicalize",
        "cse",
        "func.func(tpu-infer-vector-layout{sublane-count=8 lane-count=128})",
    ]
    pipeline = PassManager.parse(f"builtin.module({','.join(pipeline)})")
    pipeline.run(module.operation)
    module.operation.verify()

    apply_vector_layout.apply(module, hardware_generation)
    module.operation.verify()

    PassManager.parse("builtin.module(canonicalize)").run(module.operation)

    vector_constants = []
    for f in module.body:
      if "vector_constants" not in f.attributes:
        continue
      if f.name.value != "main":
        raise NotImplementedError(
            "Only the main function can have non-splat vector constants"
        )
      constant_attrs = ir.ArrayAttr(f.attributes["vector_constants"])
      del f.attributes["vector_constants"]
      for c in constant_attrs:
        c = ir.DenseElementsAttr(c)
        constant_type = ir.VectorType(c.type)
        if constant_type.element_type == ir.IntegerType.get_signless(32):
          dtype = np.int32
        elif ir.F32Type.isinstance(constant_type.element_type):
          dtype = np.float32
        else:
          raise NotImplementedError(constant_type.element_type)
        if np.issubdtype(dtype, np.integer):
          c = ir.DenseIntElementsAttr(c)
        elif np.issubdtype(dtype, np.floating):
          c = ir.DenseFPElementsAttr(c)
        else:
          raise NotImplementedError(dtype)
        vector_constants.append(
            np.asarray(c, dtype=dtype).reshape(constant_type.shape))
    bytecode_buffer = io.BytesIO()
    module.operation.write_bytecode(bytecode_buffer, desired_version=0)
    return bytecode_buffer.getvalue(), tuple(vector_constants)
