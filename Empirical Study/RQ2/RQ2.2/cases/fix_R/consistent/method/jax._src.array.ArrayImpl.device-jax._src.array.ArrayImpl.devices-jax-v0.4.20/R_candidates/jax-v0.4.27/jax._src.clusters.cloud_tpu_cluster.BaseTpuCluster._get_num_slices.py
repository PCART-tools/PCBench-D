  @staticmethod
  def _get_num_slices() -> int:
    if has_megascale_address():
      return int(get_tpu_env_value('MEGASCALE_NUM_SLICES'))
    else:
      return 1
