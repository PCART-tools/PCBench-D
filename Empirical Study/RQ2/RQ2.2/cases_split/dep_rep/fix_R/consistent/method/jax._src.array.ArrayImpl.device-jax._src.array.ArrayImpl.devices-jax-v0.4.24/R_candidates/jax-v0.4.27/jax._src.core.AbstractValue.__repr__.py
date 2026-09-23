  def __repr__(self):
    try:
      kv_pairs = (f'{k}={v}' for k, v in self.__dict__.items())
      return '{}({})'.format(self.__class__.__name__, ','.join(kv_pairs))
    except AttributeError:
      return self.__class__.__name__
