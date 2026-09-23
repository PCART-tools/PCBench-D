def _shardings_to_mlir_shardings(
    shardings: Optional[Sequence[PartitionsOrReplicated]]
    ) -> Optional[Sequence[Optional[xc.OpSharding]]]:
  if shardings is None:
    return None
  return [xla.sharding_to_proto(s) for s in shardings]
