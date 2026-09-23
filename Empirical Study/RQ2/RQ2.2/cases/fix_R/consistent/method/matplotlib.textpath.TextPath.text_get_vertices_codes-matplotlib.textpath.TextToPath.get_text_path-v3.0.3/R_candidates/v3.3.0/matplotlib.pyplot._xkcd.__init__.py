    def __init__(self, scale, length, randomness):
        self._orig = rcParams.copy()

        if rcParams['text.usetex']:
            raise RuntimeError(
                "xkcd mode is not compatible with text.usetex = True")

        from matplotlib import patheffects
        rcParams.update({
            'font.family': ['xkcd', 'xkcd Script', 'Humor Sans', 'Comic Neue',
                            'Comic Sans MS'],
            'font.size': 14.0,
            'path.sketch': (scale, length, randomness),
            'path.effects': [
                patheffects.withStroke(linewidth=4, foreground="w")],
            'axes.linewidth': 1.5,
            'lines.linewidth': 2.0,
            'figure.facecolor': 'white',
            'grid.linewidth': 0.0,
            'axes.grid': False,
            'axes.unicode_minus': False,
            'axes.edgecolor': 'black',
            'xtick.major.size': 8,
            'xtick.major.width': 3,
            'ytick.major.size': 8,
            'ytick.major.width': 3,
        })
