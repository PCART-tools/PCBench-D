@_copy_docstring_and_deprecators(FigureCanvasBase.mpl_connect)
def connect(s, func):
    return gcf().canvas.mpl_connect(s, func)
