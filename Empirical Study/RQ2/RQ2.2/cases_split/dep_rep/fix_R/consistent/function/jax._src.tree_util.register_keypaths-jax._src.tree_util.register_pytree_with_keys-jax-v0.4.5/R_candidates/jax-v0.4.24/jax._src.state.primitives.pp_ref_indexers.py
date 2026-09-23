def pp_ref_indexers(context: core.JaxprPpContext, ref, indexers):
  return pp_ref_var(
      pp.concat([
          pp.text(core.pp_var(ref, context)),
          _pp_indexers(context, indexers),
      ])
  )
