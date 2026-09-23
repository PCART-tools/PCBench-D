    def __init__(self, ax, direction):
        _api.check_in_list(self._get_func_map, direction=direction)
        self._ax_list = [ax] if isinstance(ax, Axes) else ax
        self._direction = direction
