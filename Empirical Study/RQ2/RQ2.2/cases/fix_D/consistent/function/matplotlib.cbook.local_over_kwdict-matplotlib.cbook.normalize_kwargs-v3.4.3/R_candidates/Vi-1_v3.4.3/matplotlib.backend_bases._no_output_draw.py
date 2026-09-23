def _no_output_draw(figure):
    renderer = _get_renderer(figure)
    with renderer._draw_disabled():
        figure.draw(renderer)
