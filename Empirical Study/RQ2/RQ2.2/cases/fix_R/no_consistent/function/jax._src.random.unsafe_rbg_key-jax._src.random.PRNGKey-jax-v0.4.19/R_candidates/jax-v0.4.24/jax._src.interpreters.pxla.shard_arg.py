def shard_arg(arg, sharding, canonicalize=True):
  if canonicalize:
    arg = xla.canonicalize_dtype(arg)
  return shard_arg_handlers[type(arg)](arg, sharding)
