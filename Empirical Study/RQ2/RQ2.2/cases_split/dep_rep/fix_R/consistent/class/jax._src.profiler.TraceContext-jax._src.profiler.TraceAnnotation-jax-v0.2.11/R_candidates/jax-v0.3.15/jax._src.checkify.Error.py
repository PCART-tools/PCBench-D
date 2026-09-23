@dataclass(frozen=True)
class Error:
  err: Bool
  code: Int
  msgs: Dict[int, str]
  # There might be many msgs with a {payload}, but only one msg will
  # ever be active for an Error instance, so only one Payload is tracked.
  payload: Payload = init_payload

  def get(self) -> Optional[str]:
    """Returns error message is error happened, None if no error happened."""
    assert np.shape(self.err) == np.shape(self.code)
    if np.size(self.err) == 1:
      if self.err:
        return _format_msg(self.msgs[int(self.code)], self.payload)
    else:
      return '\n'.join(
          f'at mapped index {", ".join(map(str, idx))}: '  # type: ignore
          f'{_format_msg(self.msgs[int(self.code[idx])], self.payload[idx])}'  # type: ignore
          for idx, e in np.ndenumerate(self.err) if e) or None
    return None

  def throw(self):
    """Throw ValueError with error message if error happened."""
    err = self.get()
    if err:
      raise ValueError(err)
