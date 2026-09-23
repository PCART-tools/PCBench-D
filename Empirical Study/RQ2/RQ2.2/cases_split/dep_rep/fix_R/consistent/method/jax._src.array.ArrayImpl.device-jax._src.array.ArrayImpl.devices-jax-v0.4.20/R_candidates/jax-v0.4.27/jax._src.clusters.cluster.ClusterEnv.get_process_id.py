  @classmethod
  def get_process_id(cls) -> int:
    raise NotImplementedError("ClusterEnv subclasses must implement get_process_id")
