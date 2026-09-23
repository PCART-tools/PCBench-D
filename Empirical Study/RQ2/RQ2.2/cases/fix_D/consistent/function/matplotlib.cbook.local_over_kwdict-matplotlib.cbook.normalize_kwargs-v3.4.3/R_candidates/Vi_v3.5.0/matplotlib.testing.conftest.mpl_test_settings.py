@pytest.fixture(autouse=True)
def mpl_test_settings(request):
    from matplotlib.testing.decorators import _cleanup_cm

    with _cleanup_cm():

        backend = None
        backend_marker = request.node.get_closest_marker('backend')
        if backend_marker is not None:
            assert len(backend_marker.args) == 1, \
                "Marker 'backend' must specify 1 backend."
            backend, = backend_marker.args
            skip_on_importerror = backend_marker.kwargs.get(
                'skip_on_importerror', False)
            prev_backend = matplotlib.get_backend()

            # special case Qt backend importing to avoid conflicts
            if backend.lower().startswith('qt5'):
                if any(sys.modules.get(k) for k in ('PyQt4', 'PySide')):
                    pytest.skip('Qt4 binding already imported')

        # Default of cleanup and image_comparison too.
        style = ["classic", "_classic_test_patch"]
        style_marker = request.node.get_closest_marker('style')
        if style_marker is not None:
            assert len(style_marker.args) == 1, \
                "Marker 'style' must specify 1 style."
            _api.warn_deprecated("3.5", name="style", obj_type="pytest marker",
                                 alternative="@mpl.style.context(...)")
            style, = style_marker.args

        matplotlib.testing.setup()
        with _api.suppress_matplotlib_deprecation_warning():
            if backend is not None:
                # This import must come after setup() so it doesn't load the
                # default backend prematurely.
                import matplotlib.pyplot as plt
                try:
                    plt.switch_backend(backend)
                except ImportError as exc:
                    # Should only occur for the cairo backend tests, if neither
                    # pycairo nor cairocffi are installed.
                    if 'cairo' in backend.lower() or skip_on_importerror:
                        pytest.skip("Failed to switch to backend {} ({})."
                                    .format(backend, exc))
                    else:
                        raise
            matplotlib.style.use(style)
        try:
            yield
        finally:
            if backend is not None:
                plt.switch_backend(prev_backend)
