  @staticmethod
  def _get_process_id_in_slice() -> int:
    return int(get_metadata('agent-worker-number')[0])
