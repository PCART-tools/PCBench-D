def in_interactive_session():
    """ check if we're running in an interactive shell

    returns True if running under python/ipython interactive shell
    """

    def check_main():
        import __main__ as main
        return (not hasattr(main, '__file__') or
                get_option('mode.sim_interactive'))

    try:
        return __IPYTHON__ or check_main()  # noqa
    except:
        return check_main()
