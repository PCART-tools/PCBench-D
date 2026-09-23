    @classmethod
    def _from_axes(cls, data, axes):
        # for construction from BlockManager
        if isinstance(data, BlockManager):
            return cls(data)
        else:
            if cls._AXIS_REVERSED:
                axes = axes[::-1]
            d = cls._construct_axes_dict_from(cls, axes, copy=False)
            return cls(data, **d)
