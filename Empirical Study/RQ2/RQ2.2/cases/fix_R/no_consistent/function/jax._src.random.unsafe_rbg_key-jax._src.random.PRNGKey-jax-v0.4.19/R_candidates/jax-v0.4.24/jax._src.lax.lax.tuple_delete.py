def tuple_delete(tup, idx):
  idx_ = set(idx)
  return tuple(tup[i] for i in range(len(tup)) if i not in idx_)
