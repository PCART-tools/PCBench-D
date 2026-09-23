  @classmethod
  def get_process_count(cls) -> int:
    processes_per_slice = len(cls._get_worker_list_in_slice())
    num_slices = cls._get_num_slices()
    total_process_count = processes_per_slice * num_slices
    logger.debug("Total process count of %s = %s processes per slice and %s slices", total_process_count, processes_per_slice, num_slices)
    return total_process_count
