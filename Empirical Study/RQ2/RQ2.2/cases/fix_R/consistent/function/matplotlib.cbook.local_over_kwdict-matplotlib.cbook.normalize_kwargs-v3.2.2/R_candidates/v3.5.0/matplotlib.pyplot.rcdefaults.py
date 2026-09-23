@_copy_docstring_and_deprecators(matplotlib.rcdefaults)
def rcdefaults():
    matplotlib.rcdefaults()
    if matplotlib.is_interactive():
        draw_all()
