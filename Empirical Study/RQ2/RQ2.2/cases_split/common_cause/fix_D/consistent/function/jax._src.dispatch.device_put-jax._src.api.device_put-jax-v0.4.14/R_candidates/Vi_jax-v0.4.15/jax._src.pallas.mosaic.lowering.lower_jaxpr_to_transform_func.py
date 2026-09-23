def lower_jaxpr_to_transform_func(
    ctx: ir.Context, jaxpr: jax_core.Jaxpr, memspaces: Sequence[Any],
    *, name: str) -> func.FuncOp:
  block_shapes = [i.aval.shape for i in jaxpr.invars]
  arg_types = [*map(aval_to_ir_type, [invar.aval for invar in jaxpr.invars],
                    block_shapes, memspaces)]
  lowering_context = LoweringContext(
      ctx, None, None, block_shapes, source_info_util.NameStack())
  body_func = functools.partial(jaxpr_subcomp, lowering_context, jaxpr)
  body_func.__name__ = name
  body = func.FuncOp.from_py_func(*arg_types, name=name)(body_func)
  body.func_op.verify()
  return body.func_op
