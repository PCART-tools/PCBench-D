def sequential_vmap(f):
  f = custom_vmap(f)

  @f.def_vmap
  def rule(axis_size, in_batched, *args):
    del axis_size

    def to_map(mapped_args):
      args = tree_merge(in_batched, mapped_args, bcast_args)
      return f(*args)

    mapped_args, bcast_args = tree_split(in_batched, list(args))
    out = lax.map(to_map, mapped_args)
    out_batched = tree_map(lambda _: True, out)
    return out, out_batched

  return f
