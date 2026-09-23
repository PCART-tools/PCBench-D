  def __repr__(self):
    try:
      return (f'Shard(device={self.device!r}, index={self.index}, '
              f'replica_id={self.replica_id}, data={self.data})')
    except ValueError:
      return f'Shard(device={self.device!r}, data={self.data})'
