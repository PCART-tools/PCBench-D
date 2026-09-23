@pdot_p.def_abstract_eval
def _pdot_abstract_eval(x, y, *, axis_name, pos_contract, pos_batch, precision):
  # TODO(frostig,mattjj,jekbradbury): check inputs have given axis names?
  if not len(set(axis_name)) == len(axis_name): raise ValueError
  pos_aval = lax.dot_general_p.abstract_eval(
      x, y, dimension_numbers=[pos_contract, pos_batch],
      precision=precision, preferred_element_type=None)[0]
  common_named_shape = core.join_named_shapes(x.named_shape, y.named_shape)
  named_shape = {name: size
                 for name, size in common_named_shape.items()
                 if name not in axis_name}
  return pos_aval.update(named_shape=named_shape)
