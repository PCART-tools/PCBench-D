  def to_json(self) -> bytes:
    return (
        f'{{"flops": {self.flops}, "transcendentals": {self.transcendentals},'
        f' "bytes_accessed": {self.bytes_accessed}}}'
    ).encode('ascii')
