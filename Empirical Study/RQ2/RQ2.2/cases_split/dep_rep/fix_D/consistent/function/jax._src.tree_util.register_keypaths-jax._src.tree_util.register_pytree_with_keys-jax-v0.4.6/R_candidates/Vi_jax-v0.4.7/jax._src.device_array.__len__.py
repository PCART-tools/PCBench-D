  def __len__(self):
    try:
      return self.aval.shape[0]
    except IndexError as err:
      raise TypeError("len() of unsized object") from err  # same as numpy error
