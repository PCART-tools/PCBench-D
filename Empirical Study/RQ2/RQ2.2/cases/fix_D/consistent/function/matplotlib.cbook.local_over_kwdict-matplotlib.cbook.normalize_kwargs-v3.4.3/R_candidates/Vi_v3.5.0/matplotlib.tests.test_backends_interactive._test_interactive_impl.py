def _test_interactive_impl():
    import importlib.util
    import io
    import json
    import sys
    from unittest import TestCase

    import matplotlib as mpl
    from matplotlib import pyplot as plt, rcParams
    from matplotlib.backend_bases import FigureCanvasBase

    rcParams.update({
        "webagg.open_in_browser": False,
        "webagg.port_retries": 1,
    })
    if len(sys.argv) >= 2:  # Second argument is json-encoded rcParams.
        rcParams.update(json.loads(sys.argv[1]))
    backend = plt.rcParams["backend"].lower()
    assert_equal = TestCase().assertEqual
    assert_raises = TestCase().assertRaises

    if backend.endswith("agg") and not backend.startswith(("gtk", "web")):
        # Force interactive framework setup.
        plt.figure()

        # Check that we cannot switch to a backend using another interactive
        # framework, but can switch to a backend using cairo instead of agg,
        # or a non-interactive backend.  In the first case, we use tkagg as
        # the "other" interactive backend as it is (essentially) guaranteed
        # to be present.  Moreover, don't test switching away from gtk3 (as
        # Gtk.main_level() is not set up at this point yet) and webagg (which
        # uses no interactive framework).

        if backend != "tkagg":
            with assert_raises(ImportError):
                mpl.use("tkagg", force=True)

        def check_alt_backend(alt_backend):
            mpl.use(alt_backend, force=True)
            fig = plt.figure()
            assert_equal(
                type(fig.canvas).__module__,
                "matplotlib.backends.backend_{}".format(alt_backend))

        if importlib.util.find_spec("cairocffi"):
            check_alt_backend(backend[:-3] + "cairo")
        check_alt_backend("svg")

    mpl.use(backend, force=True)

    fig, ax = plt.subplots()
    assert_equal(
        type(fig.canvas).__module__,
        "matplotlib.backends.backend_{}".format(backend))

    ax.plot([0, 1], [2, 3])

    timer = fig.canvas.new_timer(1.)  # Test floats casting to int as needed.
    timer.add_callback(FigureCanvasBase.key_press_event, fig.canvas, "q")
    # Trigger quitting upon draw.
    fig.canvas.mpl_connect("draw_event", lambda event: timer.start())
    fig.canvas.mpl_connect("close_event", print)

    result = io.BytesIO()
    fig.savefig(result, format='png')

    plt.show()

    # Ensure that the window is really closed.
    plt.pause(0.5)

    # Test that saving works after interactive window is closed, but the figure
    # is not deleted.
    result_after = io.BytesIO()
    fig.savefig(result_after, format='png')

    if not backend.startswith('qt5') and sys.platform == 'darwin':
        # FIXME: This should be enabled everywhere once Qt5 is fixed on macOS
        # to not resize incorrectly.
        assert_equal(result.getvalue(), result_after.getvalue())
