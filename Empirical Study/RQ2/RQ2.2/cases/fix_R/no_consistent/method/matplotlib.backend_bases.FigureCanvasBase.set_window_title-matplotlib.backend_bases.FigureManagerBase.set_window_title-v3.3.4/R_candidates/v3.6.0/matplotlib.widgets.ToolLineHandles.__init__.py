    def __init__(self, ax, positions, direction, line_props=None,
                 useblit=True):
        self.ax = ax

        _api.check_in_list(['horizontal', 'vertical'], direction=direction)
        self._direction = direction

        if line_props is None:
            line_props = {}
        line_props.update({'visible': False, 'animated': useblit})

        line_fun = ax.axvline if self.direction == 'horizontal' else ax.axhline

        self._artists = [line_fun(p, **line_props) for p in positions]
