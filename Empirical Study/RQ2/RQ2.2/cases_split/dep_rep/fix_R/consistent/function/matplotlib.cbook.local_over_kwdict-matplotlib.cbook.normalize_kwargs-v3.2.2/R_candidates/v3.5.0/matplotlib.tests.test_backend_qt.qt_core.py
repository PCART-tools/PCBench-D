@pytest.fixture
def qt_core(request):
    backend, = request.node.get_closest_marker('backend').args
    qt_compat = pytest.importorskip('matplotlib.backends.qt_compat')
    QtCore = qt_compat.QtCore

    return QtCore
