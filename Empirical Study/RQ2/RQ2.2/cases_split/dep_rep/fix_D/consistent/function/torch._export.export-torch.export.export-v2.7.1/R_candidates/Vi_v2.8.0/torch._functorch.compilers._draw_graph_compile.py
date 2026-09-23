def _draw_graph_compile(fx_g, _, name, clear_meta=True):
    print(fx_g.code)
    draw_graph(fx_g, name, clear_meta=clear_meta)
    return fx_g
