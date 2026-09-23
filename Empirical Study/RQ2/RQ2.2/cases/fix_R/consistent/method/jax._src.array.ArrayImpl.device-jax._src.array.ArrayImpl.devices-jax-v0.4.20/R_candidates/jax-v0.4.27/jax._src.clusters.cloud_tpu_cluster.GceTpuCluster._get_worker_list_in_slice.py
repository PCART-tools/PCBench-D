  @staticmethod
  def _get_worker_list_in_slice() -> list[str]:
    workers = get_metadata('worker-network-endpoints')[0].split(',')
    return [worker.split(':')[2] for worker in workers]
