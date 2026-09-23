def install_repl_displayhook():
    """
    Install a repl display hook so that any stale figure are automatically
    redrawn when control is returned to the repl.

    This works both with IPython and with vanilla python shells.
    """
    global _IP_REGISTERED
    global _INSTALL_FIG_OBSERVER

    if _IP_REGISTERED:
        return
    # See if we have IPython hooks around, if so use them.
    # Use ``sys.modules.get(name)`` rather than ``name in sys.modules`` as
    # entries can also have been explicitly set to None.
    mod_ipython = sys.modules.get("IPython")
    if not mod_ipython:
        _INSTALL_FIG_OBSERVER = True
        return
    ip = mod_ipython.get_ipython()
    if not ip:
        _INSTALL_FIG_OBSERVER = True
        return

    def post_execute():
        if matplotlib.is_interactive():
            draw_all()

    try:  # IPython >= 2
        ip.events.register("post_execute", post_execute)
    except AttributeError:  # IPython 1.x
        ip.register_post_execute(post_execute)
    _IP_REGISTERED = post_execute
    _INSTALL_FIG_OBSERVER = False

    from IPython.core.pylabtools import backend2gui
    # trigger IPython's eventloop integration, if available
    ipython_gui_name = backend2gui.get(get_backend())
    if ipython_gui_name:
        ip.enable_gui(ipython_gui_name)
