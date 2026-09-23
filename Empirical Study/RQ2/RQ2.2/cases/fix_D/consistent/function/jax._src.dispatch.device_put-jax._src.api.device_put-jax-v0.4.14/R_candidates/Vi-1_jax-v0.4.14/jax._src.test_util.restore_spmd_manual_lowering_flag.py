def restore_spmd_manual_lowering_flag():
  if old_spmd_manual_lowering_flag is None: return
  config.update('experimental_xmap_spmd_lowering_manual', old_spmd_manual_lowering_flag)
