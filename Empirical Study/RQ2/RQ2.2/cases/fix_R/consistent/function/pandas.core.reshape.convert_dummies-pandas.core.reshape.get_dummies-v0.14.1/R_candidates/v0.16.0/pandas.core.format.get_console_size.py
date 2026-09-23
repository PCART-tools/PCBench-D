def get_console_size():
    """Return console size as tuple = (width, height).

    Returns (None,None) in non-interactive session.
    """
    display_width = get_option('display.width')
    # deprecated.
    display_height = get_option('display.height', silent=True)

    # Consider
    # interactive shell terminal, can detect term size
    # interactive non-shell terminal (ipnb/ipqtconsole), cannot detect term
    # size non-interactive script, should disregard term size

    # in addition
    # width,height have default values, but setting to 'None' signals
    # should use Auto-Detection, But only in interactive shell-terminal.
    # Simple. yeah.

    if com.in_interactive_session():
        if com.in_ipython_frontend():
            # sane defaults for interactive non-shell terminal
            # match default for width,height in config_init
            from pandas.core.config import get_default_val
            terminal_width = get_default_val('display.width')
            terminal_height = get_default_val('display.height')
        else:
            # pure terminal
            terminal_width, terminal_height = get_terminal_size()
    else:
        terminal_width, terminal_height = None, None

    # Note if the User sets width/Height to None (auto-detection)
    # and we're in a script (non-inter), this will return (None,None)
    # caller needs to deal.
    return (display_width or terminal_width, display_height or terminal_height)
