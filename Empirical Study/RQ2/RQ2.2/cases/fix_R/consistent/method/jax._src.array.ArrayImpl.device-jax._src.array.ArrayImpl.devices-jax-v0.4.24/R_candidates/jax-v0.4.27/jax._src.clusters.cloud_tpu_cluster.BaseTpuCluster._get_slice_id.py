  @staticmethod
  def _get_slice_id() -> int:
    if has_megascale_address():
      return int(get_tpu_env_value('MEGASCALE_SLICE_ID'))
    else:
      return 0
