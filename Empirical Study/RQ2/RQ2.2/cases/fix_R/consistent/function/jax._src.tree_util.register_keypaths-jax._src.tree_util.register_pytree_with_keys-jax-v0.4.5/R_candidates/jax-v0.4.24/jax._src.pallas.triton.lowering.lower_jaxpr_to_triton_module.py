def lower_jaxpr_to_triton_module(
    jaxpr: jax_core.Jaxpr,
    in_shapes,
    grid_mapping: GridMapping,
    name: str,
    cuda_options: cb.CUDAOptions,
) -> TritonLoweringResult:
  jaxpr, _ = pe.dce_jaxpr(jaxpr, [True] * len(jaxpr.outvars), instantiate=True)
  with contextlib.ExitStack() as stack:
    builder = tc.builder(cuda_options)
    stack.enter_context(builder)
    module: ir.Module = ir.Module.create()
    stack.enter_context(ir.InsertionPoint.at_block_begin(module.body))
    param_types = [
        tc.pointer_type(_convert_dtype(var.aval.dtype)) for var in jaxpr.invars
    ]
    assert len(jaxpr.outvars) == 0
    fn_type = ir.FunctionType.get(
        [t.to_ir(builder) for t in param_types],
        [],
    )
    fn = tt_dialect.FuncOp(
        name,
        ir.TypeAttr.get(fn_type),
        sym_visibility="public",
        res_attrs=ir.DictAttr.get(dict(noinline=ir.BoolAttr.get(False))),
    )
    fn.arg_attrs = ir.ArrayAttr.get(
        [ir.DictAttr.get({"tt.divisibility": mlir.i32_attr(32)})]
        * len(param_types)
    )
    fn.body.blocks.append(*fn_type.inputs)
    [entry] = fn.body.blocks
    with ir.InsertionPoint(entry):
      new_grid, program_ids = _process_grid_to_3d_grid(grid_mapping)
      local_program_ids = [
          pid
          for i, pid in enumerate(program_ids)
          if i not in grid_mapping.mapped_dims
      ]
      ctx = TritonModuleContext(name, grid_mapping, local_program_ids)
      if grid_mapping.num_index_operands:
        raise NotImplementedError(
            "Scalar prefetch not supported in Triton lowering."
        )
      start_indices = map(
          partial(_eval_index_map, ctx, program_ids),
          grid_mapping.block_mappings,
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
      args = map(tc.tensor, entry.arguments, param_types)
      () = lower_jaxpr_to_triton_ir(ctx, jaxpr, block_infos, *args)
      tt_dialect.return_([])
    return TritonLoweringResult(module, new_grid)
