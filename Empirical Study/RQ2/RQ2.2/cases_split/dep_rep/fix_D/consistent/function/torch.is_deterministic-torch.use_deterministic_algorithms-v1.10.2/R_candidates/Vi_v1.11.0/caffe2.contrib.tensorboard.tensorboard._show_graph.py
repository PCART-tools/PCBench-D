def _show_graph(graph_def):
    import IPython.display

    code = CODE_TEMPLATE.format(
        data=repr(str(graph_def)),
        id='graph' + str(np.random.rand()),
        height=Config.HEIGHT)

    iframe = IFRAME_TEMPLATE.format(
        code=code.replace('"', '&quot;'),
        width=Config.HEIGHT * Config.ASPECT_RATIO,
        height=Config.HEIGHT + 20)

    IPython.display.display(IPython.display.HTML(iframe))
