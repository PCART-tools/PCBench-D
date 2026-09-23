def _find_partitions(jaxpr):
  """Returns (in_partitions, out_partitions, num_partitions, local_in_parts,
              local_out_parts, local_num_partitions).
  """
  for eqn in jaxpr.eqns:
    if eqn.primitive.name == "sharded_call":
      if len(jaxpr.eqns) > 1:
        raise NotImplementedError(
            "pmap of sharded_jit + non-sharded operations not yet implemented.")
      num_partitions = reconcile_num_partitions(eqn.params["call_jaxpr"],
                                                eqn.params["nparts"])
      return (eqn.params["in_parts"],
              eqn.params["out_parts_thunk"](),
              num_partitions,
              eqn.params["local_in_parts"],
              eqn.params["local_out_parts_thunk"](),
              eqn.params["local_nparts"])
  return None, None, 1, None, None, None
