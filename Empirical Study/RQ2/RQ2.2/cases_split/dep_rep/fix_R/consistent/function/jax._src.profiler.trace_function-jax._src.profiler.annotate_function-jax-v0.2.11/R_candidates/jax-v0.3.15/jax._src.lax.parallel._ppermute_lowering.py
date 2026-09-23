def _ppermute_lowering(ctx, x, *, axis_name, perm):
  replica_groups = _replica_groups(ctx.module_context.axis_env, axis_name, None)
  group_size = len(replica_groups[0])
  srcs, dsts = unzip2((src % group_size, dst % group_size) for src, dst in perm)
  if not (len(srcs) == len(set(srcs)) and len(dsts) == len(set(dsts))):
    msg = "ppermute sources and destinations must be unique, got {}."
    raise ValueError(msg.format(perm))

  full_perm = np.zeros((len(replica_groups), len(perm), 2), np.int64)
  for i, grp in enumerate(replica_groups):
    grp = list(sorted(grp))
    for j, (src, dst) in enumerate(perm):
      full_perm[i, j, 0] = grp[src]
      full_perm[i, j, 1] = grp[dst]
  full_perm = full_perm.reshape((-1, 2))
  return mhlo.CollectivePermuteOp(x, mlir.dense_int_elements(full_perm)).results
