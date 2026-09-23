def install_repl_displayhook():
    """
    Install a repl display hook so that any stale figure are automatically
    redrawn when control is returned to the repl.

    This works both with IPython and with vanilla python shells.
    """
    global _IP_REGISTERED
    global _INSTALL_FIG_OBSERVER

    class _NotIPython(Exception):
        pass

    # see if we have IPython hooks around, if use them

    try:
        if 'IPython' in sys.modules:
            from IPython import get_ipython
            ip = get_ipython()
            if ip is None:
                raise _NotIPython()

            if _IP_REGISTERED:
                return

            def post_execute():
                if matplotlib.is_interactive():
                    draw_all()

            # IPython >= 2
            try:
                ip.events.register('post_execute', post_execute)
            except AttributeError:
                # IPython 1.x
                ip.register_post_execute(post_execute)

            _IP_REGISTERED = post_execute
            _INSTALL_FIG_OBSERVER = False

            # trigger IPython's eventloop integration, if available
            from IPython.core.pylabtools import backend2gui

            ipython_gui_name = backend2gui.get(get_backend())
            if ipython_gui_name:
                ip.enable_gui(ipython_gui_name)
        else:
            _INSTALL_FIG_OBSERVER = True

    # import failed or ipython is not running
    except (ImportError, _NotIPython):
        _INSTALL_FIG_OBSERVER = True
