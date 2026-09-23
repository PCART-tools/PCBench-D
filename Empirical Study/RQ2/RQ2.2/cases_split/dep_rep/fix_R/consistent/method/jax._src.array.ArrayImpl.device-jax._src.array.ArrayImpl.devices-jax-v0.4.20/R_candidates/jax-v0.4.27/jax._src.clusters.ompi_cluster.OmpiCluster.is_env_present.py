  @classmethod
  def is_env_present(cls) -> bool:
    return _ORTE_URI in os.environ
