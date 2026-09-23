def lower_jaxpr_to_triton_module(
    jaxpr: jax_core.Jaxpr, in_shapes, grid_mapping: GridMapping, name: str
) -> tl_ir.module:
  jaxpr, _ = pe.dce_jaxpr(jaxpr, [True] * len(jaxpr.outvars), instantiate=True)
  ir_context = tl_ir.context()
  ir_context.load_triton()
  builder = tl_ir.builder(ir_context)
  # TODO(sharadmv): handle multiple devices, right now we assume device 0
  # which is fine when we have multiple of the same GPU but this won't work in
  # general.
  device = 0
  builder.arch = triton_kernel_call_lib.get_compute_capability(device)
  module = builder.create_module()
  in_avals = [var.aval for var in jaxpr.invars]
  triton_types = [get_triton_type(x) for x in in_avals]
  arg_types = [code_gen.str_to_ty(arg) for arg in triton_types]
  assert len(jaxpr.outvars) == 0
  prototype = tl.function_type([], arg_types)
  out = prototype.to_ir(builder)
  fn = builder.get_or_insert_function(module, name, out, "public", False)
  module.push_back(fn)
  entry = fn.add_entry_block()
  args = []
  for i in range(len(in_avals)):
    fn.set_arg_attr(i, "tt.divisibility", 16)
    ptr = tl.tensor(fn.args(i), prototype.param_types[i])
    args.append(ptr)
  builder.set_insertion_point_to_start(entry)
  new_grid, program_ids = _process_grid_to_3d_grid(builder, grid_mapping)
  local_program_ids = [
      pid for i, pid in enumerate(program_ids) if i not in grid_mapping.mapped_dims
  ]
  ctx = TritonModuleContext(
      name, ir_context, builder, module, grid_mapping, local_program_ids
  )
  if grid_mapping.num_index_operands:
    raise NotImplementedError(
        "Scalar prefetch not supported in Triton lowering.")
  start_indices = map(
      partial(_eval_index_map, ctx, program_ids), grid_mapping.block_mappings
  )
  block_infos = [
      BlockInfo(
          jax.ShapeDtypeStruct(shape_dtype.shape, shape_dtype.dtype),
          start_idx,
          block_mapping.block_shape,
      )
      if block_mapping is not None
      else None
      for shape_dtype, block_mapping, start_idx in zip(
          in_shapes, grid_mapping.block_mappings, start_indices
      )
  ]
  () = lower_jaxpr_to_triton_ir(ctx, jaxpr, block_infos, *args)
  module.context = ir_context
  ctx.builder.ret([])
  return TritonLoweringResult(ir_context, module, builder, new_grid)
