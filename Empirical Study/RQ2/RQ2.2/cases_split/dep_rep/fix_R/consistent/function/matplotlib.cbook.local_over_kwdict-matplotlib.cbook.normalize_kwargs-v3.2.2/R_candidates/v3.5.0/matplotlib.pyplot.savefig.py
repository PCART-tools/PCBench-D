@_copy_docstring_and_deprecators(Figure.savefig)
def savefig(*args, **kwargs):
    fig = gcf()
    res = fig.savefig(*args, **kwargs)
    fig.canvas.draw_idle()   # need this if 'transparent=True' to reset colors
    return res
