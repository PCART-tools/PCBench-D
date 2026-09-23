@_api.caching_module_getattr
class __getattr__:
    ETS = _api.deprecated("3.5")(property(lambda self: dict(
        pyqt5=(QT_API_PYQT5, 5), pyside2=(QT_API_PYSIDE2, 5))))
    QT_RC_MAJOR_VERSION = _api.deprecated("3.5")(property(
        lambda self: int(QtCore.qVersion().split(".")[0])))
