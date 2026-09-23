  @classmethod
  def get_process_count(cls) -> int:
    return int(os.environ[_PROCESS_COUNT])
