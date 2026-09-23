    def __init__(self, values, placement, ndim=None):
        """Initialize a non-consolidatable block.

        'ndim' may be inferred from 'placement'.

        This will call continue to call __init__ for the other base
        classes mixed in with this Mixin.
        """
        # Placement must be converted to BlockPlacement so that we can check
        # its length
        if not isinstance(placement, libinternals.BlockPlacement):
            placement = libinternals.BlockPlacement(placement)

        # Maybe infer ndim from placement
        if ndim is None:
            if len(placement) != 1:
                ndim = 1
            else:
                ndim = 2
        super().__init__(values, placement, ndim=ndim)
