def _get_renderer(figure, print_method=None):
    """
    Get the renderer that would be used to save a `.Figure`, and cache it on
    the figure.

    If you need a renderer without any active draw methods use
    renderer._draw_disabled to temporary patch them out at your call site.
    """
    # This is implemented by triggering a draw, then immediately jumping out of
    # Figure.draw() by raising an exception.

    class Done(Exception):
        pass

    def _draw(renderer): raise Done(renderer)

    with cbook._setattr_cm(figure, draw=_draw):
        orig_canvas = figure.canvas
        if print_method is None:
            fmt = figure.canvas.get_default_filetype()
            # Even for a canvas' default output type, a canvas switch may be
            # needed, e.g. for FigureCanvasBase.
            print_method = getattr(
                figure.canvas._get_output_canvas(None, fmt), f"print_{fmt}")
        try:
            print_method(io.BytesIO())
        except Done as exc:
            renderer, = figure._cachedRenderer, = exc.args
            return renderer
        else:
            raise RuntimeError(f"{print_method} did not call Figure.draw, so "
                               f"no renderer is available")
        finally:
            figure.canvas = orig_canvas
