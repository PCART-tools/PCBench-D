  def __lt__(self, other: ErrorEffect):
    shape_dtypes = lambda x: tuple((sd.shape, str(sd.dtype))  # dtype is not comparable
                                   for sd in x.shape_dtypes)
    unpack = lambda x: (str(x.error_type), shape_dtypes(x))
    return (unpack(self) < unpack(other))
