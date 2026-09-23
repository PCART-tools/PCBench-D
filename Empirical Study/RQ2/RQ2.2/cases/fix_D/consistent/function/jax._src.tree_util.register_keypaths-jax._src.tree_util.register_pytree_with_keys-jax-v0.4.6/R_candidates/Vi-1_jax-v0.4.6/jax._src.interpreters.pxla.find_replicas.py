def find_replicas(jaxpr, axis_size, global_axis_size):
  # TODO(skyewm): replace this with a chain of pmaps and/or sharded_jits
  jaxpr_replicas = dispatch.jaxpr_replicas(jaxpr)
  num_local_replicas = axis_size * jaxpr_replicas
  num_global_replicas = global_axis_size * jaxpr_replicas
  return ReplicaInfo(jaxpr_replicas, num_local_replicas, num_global_replicas)
