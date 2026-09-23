def are_all_shardings_default_mem_kind(da_object, shardings):
  try:
    default_mem_kind = da_object.default_memory_kind
  except:
    return True
  for i in shardings:
    if is_unspecified_or_auto(i):
      continue
    if i.memory_kind != default_mem_kind:
      return False
  return True
