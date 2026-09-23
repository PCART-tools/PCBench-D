def key_press_handler(event, canvas=None, toolbar=None):
    """
    Implement the default Matplotlib key bindings for the canvas and toolbar
    described at :ref:`key-event-handling`.

    Parameters
    ----------
    event : `KeyEvent`
        A key press/release event.
    canvas : `FigureCanvasBase`, default: ``event.canvas``
        The backend-specific canvas instance.  This parameter is kept for
        back-compatibility, but, if set, should always be equal to
        ``event.canvas``.
    toolbar : `NavigationToolbar2`, default: ``event.canvas.toolbar``
        The navigation cursor toolbar.  This parameter is kept for
        back-compatibility, but, if set, should always be equal to
        ``event.canvas.toolbar``.
    """
    # these bindings happen whether you are over an axes or not

    if event.key is None:
        return
    if canvas is None:
        canvas = event.canvas
    if toolbar is None:
        toolbar = canvas.toolbar

    # Load key-mappings from rcParams.
    fullscreen_keys = rcParams['keymap.fullscreen']
    home_keys = rcParams['keymap.home']
    back_keys = rcParams['keymap.back']
    forward_keys = rcParams['keymap.forward']
    pan_keys = rcParams['keymap.pan']
    zoom_keys = rcParams['keymap.zoom']
    save_keys = rcParams['keymap.save']
    quit_keys = rcParams['keymap.quit']
    quit_all_keys = rcParams['keymap.quit_all']
    grid_keys = rcParams['keymap.grid']
    grid_minor_keys = rcParams['keymap.grid_minor']
    toggle_yscale_keys = rcParams['keymap.yscale']
    toggle_xscale_keys = rcParams['keymap.xscale']
    all_keys = dict.__getitem__(rcParams, 'keymap.all_axes')

    # toggle fullscreen mode ('f', 'ctrl + f')
    if event.key in fullscreen_keys:
        try:
            canvas.manager.full_screen_toggle()
        except AttributeError:
            pass

    # quit the figure (default key 'ctrl+w')
    if event.key in quit_keys:
        Gcf.destroy_fig(canvas.figure)
    if event.key in quit_all_keys:
        Gcf.destroy_all()

    if toolbar is not None:
        # home or reset mnemonic  (default key 'h', 'home' and 'r')
        if event.key in home_keys:
            toolbar.home()
        # forward / backward keys to enable left handed quick navigation
        # (default key for backward: 'left', 'backspace' and 'c')
        elif event.key in back_keys:
            toolbar.back()
        # (default key for forward: 'right' and 'v')
        elif event.key in forward_keys:
            toolbar.forward()
        # pan mnemonic (default key 'p')
        elif event.key in pan_keys:
            toolbar.pan()
            toolbar._update_cursor(event)
        # zoom mnemonic (default key 'o')
        elif event.key in zoom_keys:
            toolbar.zoom()
            toolbar._update_cursor(event)
        # saving current figure (default key 's')
        elif event.key in save_keys:
            toolbar.save_figure()

    if event.inaxes is None:
        return

    # these bindings require the mouse to be over an axes to trigger
    def _get_uniform_gridstate(ticks):
        # Return True/False if all grid lines are on or off, None if they are
        # not all in the same state.
        if all(tick.gridline.get_visible() for tick in ticks):
            return True
        elif not any(tick.gridline.get_visible() for tick in ticks):
            return False
        else:
            return None

    ax = event.inaxes
    # toggle major grids in current axes (default key 'g')
    # Both here and below (for 'G'), we do nothing if *any* grid (major or
    # minor, x or y) is not in a uniform state, to avoid messing up user
    # customization.
    if (event.key in grid_keys
            # Exclude minor grids not in a uniform state.
            and None not in [_get_uniform_gridstate(ax.xaxis.minorTicks),
                             _get_uniform_gridstate(ax.yaxis.minorTicks)]):
        x_state = _get_uniform_gridstate(ax.xaxis.majorTicks)
        y_state = _get_uniform_gridstate(ax.yaxis.majorTicks)
        cycle = [(False, False), (True, False), (True, True), (False, True)]
        try:
            x_state, y_state = (
                cycle[(cycle.index((x_state, y_state)) + 1) % len(cycle)])
        except ValueError:
            # Exclude major grids not in a uniform state.
            pass
        else:
            # If turning major grids off, also turn minor grids off.
            ax.grid(x_state, which="major" if x_state else "both", axis="x")
            ax.grid(y_state, which="major" if y_state else "both", axis="y")
            canvas.draw_idle()
    # toggle major and minor grids in current axes (default key 'G')
    if (event.key in grid_minor_keys
            # Exclude major grids not in a uniform state.
            and None not in [_get_uniform_gridstate(ax.xaxis.majorTicks),
                             _get_uniform_gridstate(ax.yaxis.majorTicks)]):
        x_state = _get_uniform_gridstate(ax.xaxis.minorTicks)
        y_state = _get_uniform_gridstate(ax.yaxis.minorTicks)
        cycle = [(False, False), (True, False), (True, True), (False, True)]
        try:
            x_state, y_state = (
                cycle[(cycle.index((x_state, y_state)) + 1) % len(cycle)])
        except ValueError:
            # Exclude minor grids not in a uniform state.
            pass
        else:
            ax.grid(x_state, which="both", axis="x")
            ax.grid(y_state, which="both", axis="y")
            canvas.draw_idle()
    # toggle scaling of y-axes between 'log and 'linear' (default key 'l')
    elif event.key in toggle_yscale_keys:
        scale = ax.get_yscale()
        if scale == 'log':
            ax.set_yscale('linear')
            ax.figure.canvas.draw_idle()
        elif scale == 'linear':
            try:
                ax.set_yscale('log')
            except ValueError as exc:
                _log.warning(str(exc))
                ax.set_yscale('linear')
            ax.figure.canvas.draw_idle()
    # toggle scaling of x-axes between 'log and 'linear' (default key 'k')
    elif event.key in toggle_xscale_keys:
        scalex = ax.get_xscale()
        if scalex == 'log':
            ax.set_xscale('linear')
            ax.figure.canvas.draw_idle()
        elif scalex == 'linear':
            try:
                ax.set_xscale('log')
            except ValueError as exc:
                _log.warning(str(exc))
                ax.set_xscale('linear')
            ax.figure.canvas.draw_idle()
    # enable navigation for all axes that contain the event (default key 'a')
    elif event.key in all_keys:
        for a in canvas.figure.get_axes():
            if (event.x is not None and event.y is not None
                    and a.in_axes(event)):  # FIXME: Why only these?
                _api.warn_deprecated(
                    "3.3", message="Toggling axes navigation from the "
                    "keyboard is deprecated since %(since)s and will be "
                    "removed %(removal)s.")
                a.set_navigate(True)
    # enable navigation only for axes with this index (if such an axes exist,
    # otherwise do nothing)
    elif event.key.isdigit() and event.key != '0':
        n = int(event.key) - 1
        if n < len(canvas.figure.get_axes()):
            for i, a in enumerate(canvas.figure.get_axes()):
                if (event.x is not None and event.y is not None
                        and a.in_axes(event)):  # FIXME: Why only these?
                    _api.warn_deprecated(
                        "3.3", message="Toggling axes navigation from the "
                        "keyboard is deprecated since %(since)s and will be "
                        "removed %(removal)s.")
                    a.set_navigate(i == n)
