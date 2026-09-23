def _pp_xla_call(eqn: core.JaxprEqn, context: core.JaxprPpContext,
                 settings: core.JaxprPpSettings,
                 ) -> pp.Doc:
  printed_params = {k:v for k, v in eqn.params.items() if
                    k == 'call_jaxpr' or k == 'name' or
                    k == 'backend' and v is not None or
                    k == 'device' and v is not None or
                    k == 'donated_invars' and any(v)}
  return core._pp_eqn(eqn.replace(params=printed_params), context, settings)
