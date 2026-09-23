class ReplicaInfo(NamedTuple):
  jaxpr_replicas: int
  num_local_replicas: int
  num_global_replicas: int
