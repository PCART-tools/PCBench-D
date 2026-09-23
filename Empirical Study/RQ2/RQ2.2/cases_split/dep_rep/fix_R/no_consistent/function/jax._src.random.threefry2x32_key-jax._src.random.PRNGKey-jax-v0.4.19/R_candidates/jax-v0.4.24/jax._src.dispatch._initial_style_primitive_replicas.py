def _initial_style_primitive_replicas(params: dict[str, Any]) -> int:
  return max(core.traverse_jaxpr_params(jaxpr_replicas, params).values(),
             default=1)
