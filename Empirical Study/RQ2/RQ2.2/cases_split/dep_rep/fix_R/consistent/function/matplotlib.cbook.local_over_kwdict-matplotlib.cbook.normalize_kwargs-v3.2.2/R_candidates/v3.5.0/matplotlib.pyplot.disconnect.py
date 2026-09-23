@_copy_docstring_and_deprecators(FigureCanvasBase.mpl_disconnect)
def disconnect(cid):
    return gcf().canvas.mpl_disconnect(cid)
