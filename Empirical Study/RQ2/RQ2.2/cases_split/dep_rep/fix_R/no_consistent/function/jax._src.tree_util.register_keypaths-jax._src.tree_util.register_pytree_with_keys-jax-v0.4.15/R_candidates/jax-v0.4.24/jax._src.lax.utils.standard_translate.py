def standard_translate(prim):
  xla_opname = ''.join(term.capitalize() for term in prim.name.split('_'))
  op = getattr(xops, xla_opname)
  def translation_rule(ctx, avals_in, avals_out, *args, **kwargs):
    del ctx, avals_in, avals_out
    return [op(*args, **kwargs)]
  return translation_rule
