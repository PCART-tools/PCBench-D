  @classmethod
  def get_process_id(cls) -> int:
    return int(os.environ[_PROCESS_ID])
