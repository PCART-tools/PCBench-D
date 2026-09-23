  def __init__(self, *args, **kwargs):
    self.__positional = canonicalize_shape(args)
    # TODO: Assert that kwargs match axis env?
    self.__named = dict(kwargs)
