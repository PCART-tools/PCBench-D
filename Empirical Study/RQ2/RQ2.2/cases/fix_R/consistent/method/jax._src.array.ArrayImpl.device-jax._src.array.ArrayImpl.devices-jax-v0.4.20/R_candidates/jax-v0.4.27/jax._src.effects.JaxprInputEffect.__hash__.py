  def __hash__(self):
    return hash((self.__class__, self.input_index))
