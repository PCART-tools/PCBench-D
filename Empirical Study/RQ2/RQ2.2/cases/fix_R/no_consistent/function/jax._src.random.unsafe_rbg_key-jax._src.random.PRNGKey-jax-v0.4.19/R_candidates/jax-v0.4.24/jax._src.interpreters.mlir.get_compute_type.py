def get_compute_type(memory_kind: str) -> str:
  if memory_kind == 'tpu_hbm':
    return 'dense'
  elif memory_kind == 'unpinned_host':
    return 'host'
  raise ValueError(f'Unknown memory_kind: {memory_kind}')
