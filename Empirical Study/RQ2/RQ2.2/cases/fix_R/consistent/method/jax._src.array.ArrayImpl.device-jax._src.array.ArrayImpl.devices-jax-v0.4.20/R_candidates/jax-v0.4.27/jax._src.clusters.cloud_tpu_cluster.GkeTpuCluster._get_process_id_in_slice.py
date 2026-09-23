  @staticmethod
  def _get_process_id_in_slice() -> int:
    return int(str(os.environ.get('TPU_WORKER_ID')))
