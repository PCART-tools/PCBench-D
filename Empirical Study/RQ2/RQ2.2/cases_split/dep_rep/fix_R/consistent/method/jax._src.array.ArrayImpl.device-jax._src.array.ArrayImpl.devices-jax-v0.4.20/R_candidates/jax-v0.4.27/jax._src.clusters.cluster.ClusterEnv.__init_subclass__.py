  def __init_subclass__(cls, **kwargs):
    super().__init_subclass__(**kwargs)
    cls._cluster_types.append(cls)
