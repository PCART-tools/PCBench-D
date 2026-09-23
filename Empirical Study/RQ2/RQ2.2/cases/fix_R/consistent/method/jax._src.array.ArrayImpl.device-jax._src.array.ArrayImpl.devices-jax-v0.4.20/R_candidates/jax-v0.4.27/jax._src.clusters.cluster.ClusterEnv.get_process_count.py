  @classmethod
  def get_process_count(cls) -> int:
    raise NotImplementedError("ClusterEnv subclasses must implement get_process_count")
