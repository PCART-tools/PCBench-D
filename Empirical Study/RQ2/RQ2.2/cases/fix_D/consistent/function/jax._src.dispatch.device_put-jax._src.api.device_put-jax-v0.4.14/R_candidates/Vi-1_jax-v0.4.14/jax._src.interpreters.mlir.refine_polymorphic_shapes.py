def refine_polymorphic_shapes(module: ir.Module) -> ir.Module:
  """Refines the polymorphic shapes inside a module.

  Given a module with static input shapes, but using dynamic shapes due to
  shape polymorphism, runs shape refinement to resolve all the dynamic shapes.
  Then verifies that there are no more dynamic shapes in the module.
  """
  if xc.mlir_api_version >= 53:
    refined_module_str = xla_extension.mlir.refine_polymorphic_shapes(
      module_to_bytecode(module), enable_shape_assertions=True,
      validate_static_shapes=True)
  elif xc.mlir_api_version == 52:
    refined_module_str = xla_extension.mlir.refine_polymorphic_shapes(
      module_to_bytecode(module), enable_shape_assertions=True)
  elif xc.mlir_api_version >= 50:
    refined_module_str = xla_extension.mlir.refine_polymorphic_shapes(
      module_to_bytecode(module))
  else:
    raise NotImplementedError("refine_polymorphic_shapes needs jaxlib 0.4.12")

  context = make_ir_context()
  with context:
    return ir.Module.parse(refined_module_str)
