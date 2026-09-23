@_copy_docstring_and_deprecators(Figure.ginput)
def ginput(
        n=1, timeout=30, show_clicks=True,
        mouse_add=MouseButton.LEFT, mouse_pop=MouseButton.RIGHT,
        mouse_stop=MouseButton.MIDDLE):
    return gcf().ginput(
        n=n, timeout=timeout, show_clicks=show_clicks,
        mouse_add=mouse_add, mouse_pop=mouse_pop,
        mouse_stop=mouse_stop)
