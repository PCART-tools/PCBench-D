def jaxpr_replicas(jaxpr: core.Jaxpr) -> int:
  """The number of replicas needed for a jaxpr.

  For a eqn, multiply the `axis_size` with the `jaxpr_replicas` of the
  subjaxprs. For a list of eqns, take the maximum number of replicas.
  """
  return max(unsafe_map(_eqn_replicas, jaxpr.eqns), default=1)
