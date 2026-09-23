def jaxpr_shardings(
    jaxpr: core.Jaxpr,
) -> Iterator[tuple[XLACompatibleSharding, SourceInfo]]:
  from jax._src import pjit
  from jax.experimental import shard_map

  for eqn in jaxpr.eqns:
    if eqn.primitive is pjit.sharding_constraint_p:
      source_info = SourceInfo(source_info_util.summarize(eqn.source_info),
                                eqn.primitive.name)
      yield (eqn.params['sharding'], source_info)
    elif eqn.primitive is pjit.pjit_p:
      source_info = SourceInfo(source_info_util.summarize(eqn.source_info),
                                eqn.primitive.name)
      yield from ((i, source_info) for i in eqn.params['in_shardings'])
      yield from ((o, source_info) for o in eqn.params['out_shardings'])
    elif eqn.primitive is shard_map.shard_map_p:
      source_info = SourceInfo(source_info_util.summarize(eqn.source_info),
                                eqn.primitive.name)
      def _names_to_pspec(names):
        ndmin = max(names) + 1 if names else 0
        return PartitionSpec(*(names.get(i) for i in range(ndmin)))
      yield from ((NamedSharding(eqn.params['mesh'], _names_to_pspec(names)), source_info)
                  for names in [*eqn.params['in_names'], *eqn.params['out_names']])
    elif eqn.primitive is device_put_p:
      s = eqn.params['device']
      if isinstance(s, XLACompatibleSharding) and s.memory_kind is not None:
        source_info = SourceInfo(source_info_util.summarize(eqn.source_info),
                                 eqn.primitive.name)
        yield (s, source_info)
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from jaxpr_shardings(subjaxpr)
