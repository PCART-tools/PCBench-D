def restore_spmd_lowering_flag():
  if old_spmd_lowering_flag is None: return
  config.update('experimental_xmap_spmd_lowering', old_spmd_lowering_flag)
