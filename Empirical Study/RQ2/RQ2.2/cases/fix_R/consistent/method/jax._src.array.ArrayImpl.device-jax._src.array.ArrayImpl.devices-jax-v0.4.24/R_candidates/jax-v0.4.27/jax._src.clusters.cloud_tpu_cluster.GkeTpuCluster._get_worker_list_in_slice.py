  @staticmethod
  def _get_worker_list_in_slice() -> list[str]:
    return str(os.environ.get('TPU_WORKER_HOSTNAMES', None)).split(',')
