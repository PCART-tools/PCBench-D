    @_api.make_keyword_only("3.7", "line_props")
    def __init__(self, ax, positions, direction, line_props=None,
                 useblit=True):
        self.ax = ax

        _api.check_in_list(['horizontal', 'vertical'], direction=direction)
        self._direction = direction

        line_props = {
            **(line_props if line_props is not None else {}),
            'visible': False,
            'animated': useblit,
        }

        line_fun = ax.axvline if self.direction == 'horizontal' else ax.axhline

        self._artists = [line_fun(p, **line_props) for p in positions]
