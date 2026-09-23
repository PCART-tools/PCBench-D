def _get_testable_interactive_backends():
    try:
        from matplotlib.backends.qt_compat import QtGui  # noqa
        have_qt5 = True
    except ImportError:
        have_qt5 = False

    backends = []
    for deps, backend in [
            (["cairo", "gi"], "gtk3agg"),
            (["cairo", "gi"], "gtk3cairo"),
            (["PyQt5"], "qt5agg"),
            (["PyQt5", "cairocffi"], "qt5cairo"),
            (["PySide2"], "qt5agg"),
            (["PySide2", "cairocffi"], "qt5cairo"),
            (["tkinter"], "tkagg"),
            (["wx"], "wx"),
            (["wx"], "wxagg"),
            (["matplotlib.backends._macosx"], "macosx"),
    ]:
        reason = None
        missing = [dep for dep in deps if not importlib.util.find_spec(dep)]
        if (sys.platform == "linux" and
                not _c_internal_utils.display_is_valid()):
            reason = "$DISPLAY and $WAYLAND_DISPLAY are unset"
        elif missing:
            reason = "{} cannot be imported".format(", ".join(missing))
        elif backend == 'macosx' and os.environ.get('TF_BUILD'):
            reason = "macosx backend fails on Azure"
        elif 'qt5' in backend and not have_qt5:
            reason = "no usable Qt5 bindings"
        marks = []
        if reason:
            marks.append(pytest.mark.skip(
                reason=f"Skipping {backend} because {reason}"))
        elif backend.startswith('wx') and sys.platform == 'darwin':
            # ignore on OSX because that's currently broken (github #16849)
            marks.append(pytest.mark.xfail(reason='github #16849'))
        backend = pytest.param(backend, marks=marks)
        backends.append(backend)
    return backends
