  def __getitem__(self, index):
    return _IndexUpdateRef(self.array, index)
