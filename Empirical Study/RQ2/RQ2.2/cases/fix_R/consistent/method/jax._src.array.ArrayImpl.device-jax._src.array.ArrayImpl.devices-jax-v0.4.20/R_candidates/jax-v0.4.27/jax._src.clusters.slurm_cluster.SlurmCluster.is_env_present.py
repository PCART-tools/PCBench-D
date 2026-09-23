  @classmethod
  def is_env_present(cls) -> bool:
    return _JOBID_PARAM in os.environ
