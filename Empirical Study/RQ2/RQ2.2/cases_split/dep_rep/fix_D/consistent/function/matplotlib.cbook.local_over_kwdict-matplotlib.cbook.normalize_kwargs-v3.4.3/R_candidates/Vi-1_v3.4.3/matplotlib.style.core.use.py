def use(style):
    """
    Use Matplotlib style settings from a style specification.

    The style name of 'default' is reserved for reverting back to
    the default style settings.

    .. note::

       This updates the `.rcParams` with the settings from the style.
       `.rcParams` not defined in the style are kept.

    Parameters
    ----------
    style : str, dict, Path or list
        A style specification. Valid options are:

        +------+-------------------------------------------------------------+
        | str  | The name of a style or a path/URL to a style file. For a    |
        |      | list of available style names, see `style.available`.       |
        +------+-------------------------------------------------------------+
        | dict | Dictionary with valid key/value pairs for                   |
        |      | `matplotlib.rcParams`.                                      |
        +------+-------------------------------------------------------------+
        | Path | A path-like object which is a path to a style file.         |
        +------+-------------------------------------------------------------+
        | list | A list of style specifiers (str, Path or dict) applied from |
        |      | first to last in the list.                                  |
        +------+-------------------------------------------------------------+

    """
    style_alias = {'mpl20': 'default',
                   'mpl15': 'classic'}
    if isinstance(style, (str, Path)) or hasattr(style, 'keys'):
        # If name is a single str, Path or dict, make it a single element list.
        styles = [style]
    else:
        styles = style

    styles = (style_alias.get(s, s) if isinstance(s, str) else s
              for s in styles)
    for style in styles:
        if not isinstance(style, (str, Path)):
            _apply_style(style)
        elif style == 'default':
            # Deprecation warnings were already handled when creating
            # rcParamsDefault, no need to reemit them here.
            with _api.suppress_matplotlib_deprecation_warning():
                _apply_style(rcParamsDefault, warn=False)
        elif style in library:
            _apply_style(library[style])
        else:
            try:
                rc = rc_params_from_file(style, use_default_template=False)
                _apply_style(rc)
            except IOError as err:
                raise IOError(
                    "{!r} not found in the style library and input is not a "
                    "valid URL or path; see `style.available` for list of "
                    "available styles".format(style)) from err
