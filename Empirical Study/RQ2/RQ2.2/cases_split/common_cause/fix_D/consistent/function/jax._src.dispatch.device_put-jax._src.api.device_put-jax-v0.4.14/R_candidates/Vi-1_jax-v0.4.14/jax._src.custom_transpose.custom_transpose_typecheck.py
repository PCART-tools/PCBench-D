def custom_transpose_typecheck(_, *in_atoms, out_types, **params):
  del in_atoms, params
  return out_types, core.no_effects
