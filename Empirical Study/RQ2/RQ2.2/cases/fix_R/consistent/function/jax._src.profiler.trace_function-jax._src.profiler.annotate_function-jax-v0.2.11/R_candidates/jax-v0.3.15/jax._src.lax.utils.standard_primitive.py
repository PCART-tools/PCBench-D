def standard_primitive(shape_rule, dtype_rule, name, translation_rule=None,
                       weak_type_rule=None, named_shape_rule=None):
  weak_type_rule = weak_type_rule or _standard_weak_type_rule
  named_shape_rule = named_shape_rule or standard_named_shape_rule
  prim = core.Primitive(name)
  prim.def_impl(partial(xla.apply_primitive, prim))
  prim.def_abstract_eval(
      partial(standard_abstract_eval, prim, shape_rule, dtype_rule,
              weak_type_rule, named_shape_rule))
  if translation_rule is not None:
    xla.register_translation(prim, translation_rule)
  return prim
