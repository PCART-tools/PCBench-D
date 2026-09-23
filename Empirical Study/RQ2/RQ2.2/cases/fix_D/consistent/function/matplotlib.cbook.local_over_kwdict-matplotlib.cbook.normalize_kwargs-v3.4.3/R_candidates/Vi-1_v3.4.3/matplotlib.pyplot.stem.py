@_copy_docstring_and_deprecators(Axes.stem)
def stem(
        *args, linefmt=None, markerfmt=None, basefmt=None, bottom=0,
        label=None, use_line_collection=True, orientation='vertical',
        data=None):
    return gca().stem(
        *args, linefmt=linefmt, markerfmt=markerfmt, basefmt=basefmt,
        bottom=bottom, label=label,
        use_line_collection=use_line_collection,
        orientation=orientation,
        **({"data": data} if data is not None else {}))
