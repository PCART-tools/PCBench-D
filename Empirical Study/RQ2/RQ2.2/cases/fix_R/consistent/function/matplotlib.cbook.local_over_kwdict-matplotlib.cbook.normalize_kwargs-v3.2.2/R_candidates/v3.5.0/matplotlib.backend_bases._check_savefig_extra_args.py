def _check_savefig_extra_args(func=None, extra_kwargs=()):
    """
    Decorator for the final print_* methods that accept keyword arguments.

    If any unused keyword arguments are left, this decorator will warn about
    them, and as part of the warning, will attempt to specify the function that
    the user actually called, instead of the backend-specific method. If unable
    to determine which function the user called, it will specify `.savefig`.

    For compatibility across backends, this does not warn about keyword
    arguments added by `FigureCanvasBase.print_figure` for use in a subset of
    backends, because the user would not have added them directly.
    """

    if func is None:
        return functools.partial(_check_savefig_extra_args,
                                 extra_kwargs=extra_kwargs)

    old_sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = 'savefig'  # Reasonable default guess.
        public_api = re.compile(
            r'^savefig|print_[A-Za-z0-9]+|_no_output_draw$'
        )
        seen_print_figure = False
        for frame, line in traceback.walk_stack(None):
            if frame is None:
                # when called in embedded context may hit frame is None.
                break
            # Work around sphinx-gallery not setting __name__.
            frame_name = frame.f_globals.get('__name__', '')
            if re.match(r'\A(matplotlib|mpl_toolkits)(\Z|\.(?!tests\.))',
                        frame_name):
                name = frame.f_code.co_name
                if public_api.match(name):
                    if name in ('print_figure', '_no_output_draw'):
                        seen_print_figure = True

            elif frame_name == '_functools':
                # PyPy adds an extra frame without module prefix for this
                # functools wrapper, which we ignore to assume we're still in
                # Matplotlib code.
                continue
            else:
                break

        accepted_kwargs = {*old_sig.parameters, *extra_kwargs}
        if seen_print_figure:
            for kw in ['dpi', 'facecolor', 'edgecolor', 'orientation',
                       'bbox_inches_restore']:
                # Ignore keyword arguments that are passed in by print_figure
                # for the use of other renderers.
                if kw not in accepted_kwargs:
                    kwargs.pop(kw, None)

        for arg in list(kwargs):
            if arg in accepted_kwargs:
                continue
            _api.warn_deprecated(
                '3.3', name=name,
                message='%(name)s() got unexpected keyword argument "'
                        + arg + '" which is no longer supported as of '
                        '%(since)s and will become an error '
                        '%(removal)s')
            kwargs.pop(arg)

        return func(*args, **kwargs)

    return wrapper
