    @classmethod
    def _from_axes(cls, data, axes, **kwargs):
        # for construction from BlockManager
        if isinstance(data, BlockManager):
            return cls(data, **kwargs)
        else:
            if cls._AXIS_REVERSED:
                axes = axes[::-1]
            d = cls._construct_axes_dict_from(cls, axes, copy=False)
            d.update(kwargs)
            return cls(data, **d)
