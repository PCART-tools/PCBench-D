def uninstall_repl_displayhook():
    """
    Uninstall the matplotlib display hook.

    .. warning::

       Need IPython >= 2 for this to work.  For IPython < 2 will raise a
       ``NotImplementedError``

    .. warning::

       If you are using vanilla python and have installed another
       display hook this will reset ``sys.displayhook`` to what ever
       function was there when matplotlib installed it's displayhook,
       possibly discarding your changes.
    """
    global _IP_REGISTERED
    global _INSTALL_FIG_OBSERVER
    if _IP_REGISTERED:
        from IPython import get_ipython
        ip = get_ipython()
        try:
            ip.events.unregister('post_execute', _IP_REGISTERED)
        except AttributeError as err:
            raise NotImplementedError("Can not unregister events "
                                      "in IPython < 2.0") from err
        _IP_REGISTERED = None

    if _INSTALL_FIG_OBSERVER:
        _INSTALL_FIG_OBSERVER = False
