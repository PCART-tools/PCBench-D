@_copy_docstring_and_deprecators(Axes.eventplot)
def eventplot(
        positions, orientation='horizontal', lineoffsets=1,
        linelengths=1, linewidths=None, colors=None,
        linestyles='solid', *, data=None, **kwargs):
    return gca().eventplot(
        positions, orientation=orientation, lineoffsets=lineoffsets,
        linelengths=linelengths, linewidths=linewidths, colors=colors,
        linestyles=linestyles,
        **({"data": data} if data is not None else {}), **kwargs)
