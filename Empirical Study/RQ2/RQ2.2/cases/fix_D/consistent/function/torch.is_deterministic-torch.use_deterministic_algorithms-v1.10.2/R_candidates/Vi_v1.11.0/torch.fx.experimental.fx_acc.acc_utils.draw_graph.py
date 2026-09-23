def draw_graph(traced: torch.fx.GraphModule, fname: str, figname: str = "fx_graph"):
    base, ext = os.path.splitext(fname)
    if not ext:
        ext = ".svg"
    print(f"Writing FX graph to file: {base}{ext}")
    g = graph_drawer.FxGraphDrawer(traced, figname)
    x = g.get_main_dot_graph()
    try:
        getattr(x, "write_" + ext.lstrip("."))(fname)
    except OSError as e:
        print(f"Failed to write the FX graph due to: {e}")
