  @classmethod
  def is_env_present(cls) -> bool:
    """Returns True if process is running in this cluster environment.
    """
    raise NotImplementedError("ClusterEnv subclasses must implement is_env_present")
