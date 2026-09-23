@pytest.fixture
def qt_core(request):
    backend, = request.node.get_closest_marker('backend').args
    qt_compat = pytest.importorskip('matplotlib.backends.qt_compat')
    QtCore = qt_compat.QtCore

    if backend == 'Qt4Agg':
        try:
            py_qt_ver = int(QtCore.PYQT_VERSION_STR.split('.')[0])
        except AttributeError:
            py_qt_ver = QtCore.__version_info__[0]
        if py_qt_ver != 4:
            pytest.skip('Qt4 is not available')

    return QtCore
