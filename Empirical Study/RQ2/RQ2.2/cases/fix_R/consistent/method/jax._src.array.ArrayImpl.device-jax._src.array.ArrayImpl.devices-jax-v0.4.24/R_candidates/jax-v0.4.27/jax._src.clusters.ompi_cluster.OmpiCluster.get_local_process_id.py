  @classmethod
  def get_local_process_id(cls) -> int | None:
    return int(os.environ[_LOCAL_PROCESS_ID])
