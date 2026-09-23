@dataclasses.dataclass
class TracebackCaches:
  canonical_name_cache: dict[str, str]
  is_user_file_cache: dict[str, bool]
  raw_frame_to_frame_cache: dict[tuple[str, int], source_info_util.Frame]

  def __init__(self):
    self.canonical_name_cache = {}
    self.is_user_file_cache = {}
    self.raw_frame_to_frame_cache = {}
