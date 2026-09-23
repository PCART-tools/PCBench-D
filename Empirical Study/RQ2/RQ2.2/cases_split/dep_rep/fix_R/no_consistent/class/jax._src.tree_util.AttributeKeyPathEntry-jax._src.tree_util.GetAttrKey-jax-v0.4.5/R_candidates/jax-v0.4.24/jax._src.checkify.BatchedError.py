@dataclasses.dataclass
class BatchedError(JaxException):
  error_mapping: dict[tuple[int, ...], JaxException]

  def __post_init__(self):
    traceback_info = list(self.error_mapping.values())[0].traceback_info
    super().__init__(traceback_info)


  def __str__(self):
    return '\n'.join(f'at mapped index {", ".join(map(str, idx))}: {e}'
                     for idx, e in self.error_mapping.items())
