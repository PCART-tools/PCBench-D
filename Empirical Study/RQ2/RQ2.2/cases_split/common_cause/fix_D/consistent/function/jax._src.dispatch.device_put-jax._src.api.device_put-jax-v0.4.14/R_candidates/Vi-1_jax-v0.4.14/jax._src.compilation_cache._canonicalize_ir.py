def _canonicalize_ir(m_original: ir.Module) -> bytes:
  with m_original.context:
    m = m_original.operation.clone()
    if jaxlib_version < (0, 4, 14):
      passes = pm.PassManager.parse(
          "builtin.module(func.func(jax-strip-locations))"
      )
    else:
      passes = pm.PassManager.parse(
          "builtin.module(strip-debuginfo)"
      )
    passes.run(m.operation)
    return _serialize_ir(m)
