    def __init__(self, ax, direction):
        self._get_size = _api.check_getitem(
            self._get_size_map, direction=direction)
        self._ax_list = [ax] if isinstance(ax, Axes) else ax
