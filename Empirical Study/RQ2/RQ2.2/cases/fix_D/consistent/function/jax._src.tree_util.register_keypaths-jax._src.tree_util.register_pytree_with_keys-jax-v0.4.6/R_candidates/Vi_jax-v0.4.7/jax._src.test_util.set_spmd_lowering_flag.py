def set_spmd_lowering_flag(val: bool):
  global old_spmd_lowering_flag
  old_spmd_lowering_flag = config.experimental_xmap_spmd_lowering
  config.update('experimental_xmap_spmd_lowering', val)
