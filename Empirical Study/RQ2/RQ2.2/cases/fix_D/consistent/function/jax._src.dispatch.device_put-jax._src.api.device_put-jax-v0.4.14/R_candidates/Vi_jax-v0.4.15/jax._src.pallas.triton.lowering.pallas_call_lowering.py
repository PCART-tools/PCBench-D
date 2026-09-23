def pallas_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    jaxpr: jax_core.Jaxpr,
    name: str,
    in_shapes: Tuple[jax.ShapeDtypeStruct, ...],
    out_shapes: Tuple[jax.ShapeDtypeStruct, ...],
    which_linear: Tuple[bool, ...],
    interpret: bool,
    debug: bool,
    input_output_aliases: Tuple[Tuple[int, int], ...],
    grid_mapping: GridMapping,
    triton_params: Dict[str, Any] | None = None,
    **compiler_params: Any,
):
  if interpret:
    return mlir.lower_fun(pallas_call_p.impl, multiple_results=True)(
        ctx,
        *in_nodes,
        jaxpr=jaxpr,
        name=name,
        out_shapes=out_shapes,
        in_shapes=in_shapes,
        which_linear=which_linear,
        interpret=interpret,
        debug=debug,
        input_output_aliases=input_output_aliases,
        grid_mapping=grid_mapping,
        **compiler_params
    )
  num_warps = compiler_params.get("num_warps", 4)
  num_stages = compiler_params.get("num_stages", 3)
  if debug:
    print(jaxpr)
    print(grid_mapping)
  compilation_result = compile_jaxpr(
      jaxpr,
      tuple((*in_shapes, *out_shapes)),
      grid_mapping,
      name,
      num_warps,
      num_stages,
      debug=debug,
  )

  if debug:
    compilation_result.lowering_result.module.dump()

  kernel = triton_kernel_call_lib.TritonKernel(
      compilation_result.kernel_name,
      num_warps,
      compilation_result.shared_mem_bytes,
      compilation_result.ptx,
      compilation_result.ttir,
      compilation_result.compute_capability,
  )

  grid = triton_lib.normalize_grid(
      compilation_result.lowering_result.grid, metaparams={}
  )

  kernel_params = []
  for _ in range(len(in_shapes) + len(out_shapes)):
    kernel_params.append(
        triton_kernel_call_lib.create_array_parameter(
            0,  # bytes to zero  # TODO(cjfj): Expose through user API.
            16,  # divisible by 16
        )
    )

  kernel_call = triton_kernel_call_lib.TritonKernelCall(
      kernel, grid[0], grid[1], grid[2], kernel_params
  )

  out_types = [
      ir.RankedTensorType.get(shape.shape, mlir.dtype_to_ir_type(shape.dtype))
      for shape in out_shapes
  ]

  if triton_params is None:
    triton_params = {}
  serialized_metadata = triton_params.get("serialized_metadata", b"")
  if version >= (0, 4, 15):
    kernel_call_proto = kernel_call.to_proto(name, serialized_metadata)
  else:
    kernel_call_proto = kernel_call.to_proto(serialized_metadata)
  return hlo_helpers.custom_call(
      call_target_name="triton_kernel_call",
      out_types=out_types,
      operands=in_nodes,
      backend_config=zlib.compress(kernel_call_proto),
      operand_layouts=triton_lib.avals_to_layouts(ctx.avals_in),
      result_layouts=triton_lib.avals_to_layouts(ctx.avals_out),
      operand_output_aliases=dict(input_output_aliases),
  )
