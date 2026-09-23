@_copy_docstring_and_deprecators(Axes.stairs)
def stairs(
        values, edges=None, *, orientation='vertical', baseline=0,
        fill=False, data=None, **kwargs):
    return gca().stairs(
        values, edges=edges, orientation=orientation,
        baseline=baseline, fill=fill,
        **({"data": data} if data is not None else {}), **kwargs)
