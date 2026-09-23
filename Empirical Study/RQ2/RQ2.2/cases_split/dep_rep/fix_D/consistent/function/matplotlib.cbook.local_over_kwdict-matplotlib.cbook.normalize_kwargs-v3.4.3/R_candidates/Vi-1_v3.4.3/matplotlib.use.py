def use(backend, *, force=True):
    """
    Select the backend used for rendering and GUI integration.

    Parameters
    ----------
    backend : str
        The backend to switch to.  This can either be one of the standard
        backend names, which are case-insensitive:

        - interactive backends:
          GTK3Agg, GTK3Cairo, MacOSX, nbAgg,
          Qt4Agg, Qt4Cairo, Qt5Agg, Qt5Cairo,
          TkAgg, TkCairo, WebAgg, WX, WXAgg, WXCairo

        - non-interactive backends:
          agg, cairo, pdf, pgf, ps, svg, template

        or a string of the form: ``module://my.module.name``.

    force : bool, default: True
        If True (the default), raise an `ImportError` if the backend cannot be
        set up (either because it fails to import, or because an incompatible
        GUI interactive framework is already running); if False, ignore the
        failure.

    See Also
    --------
    :ref:`backends`
    matplotlib.get_backend
    """
    name = validate_backend(backend)
    # we need to use the base-class method here to avoid (prematurely)
    # resolving the "auto" backend setting
    if dict.__getitem__(rcParams, 'backend') == name:
        # Nothing to do if the requested backend is already set
        pass
    else:
        # if pyplot is not already imported, do not import it.  Doing
        # so may trigger a `plt.switch_backend` to the _default_ backend
        # before we get a chance to change to the one the user just requested
        plt = sys.modules.get('matplotlib.pyplot')
        # if pyplot is imported, then try to change backends
        if plt is not None:
            try:
                # we need this import check here to re-raise if the
                # user does not have the libraries to support their
                # chosen backend installed.
                plt.switch_backend(name)
            except ImportError:
                if force:
                    raise
        # if we have not imported pyplot, then we can set the rcParam
        # value which will be respected when the user finally imports
        # pyplot
        else:
            rcParams['backend'] = backend
    # if the user has asked for a given backend, do not helpfully
    # fallback
    rcParams['backend_fallback'] = False
