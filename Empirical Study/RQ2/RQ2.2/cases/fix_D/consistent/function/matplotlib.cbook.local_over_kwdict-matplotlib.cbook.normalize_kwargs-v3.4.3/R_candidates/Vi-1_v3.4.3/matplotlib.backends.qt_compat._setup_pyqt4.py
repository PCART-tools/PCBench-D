def _setup_pyqt4():
    global QtCore, QtGui, QtWidgets, __version__, is_pyqt5, \
        _isdeleted, _getSaveFileName

    def _setup_pyqt4_internal(api):
        global QtCore, QtGui, QtWidgets, \
            __version__, is_pyqt5, _isdeleted, _getSaveFileName
        # List of incompatible APIs:
        # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
        _sip_apis = ["QDate", "QDateTime", "QString", "QTextStream", "QTime",
                     "QUrl", "QVariant"]
        try:
            import sip
        except ImportError:
            pass
        else:
            for _sip_api in _sip_apis:
                try:
                    sip.setapi(_sip_api, api)
                except (AttributeError, ValueError):
                    pass
        from PyQt4 import QtCore, QtGui
        import sip  # Always succeeds *after* importing PyQt4.
        __version__ = QtCore.PYQT_VERSION_STR
        # PyQt 4.6 introduced getSaveFileNameAndFilter:
        # https://riverbankcomputing.com/news/pyqt-46
        if __version__ < LooseVersion("4.6"):
            raise ImportError("PyQt<4.6 is not supported")
        QtCore.Signal = QtCore.pyqtSignal
        QtCore.Slot = QtCore.pyqtSlot
        QtCore.Property = QtCore.pyqtProperty
        _isdeleted = sip.isdeleted
        _getSaveFileName = QtGui.QFileDialog.getSaveFileNameAndFilter

    if QT_API == QT_API_PYQTv2:
        _setup_pyqt4_internal(api=2)
    elif QT_API == QT_API_PYSIDE:
        from PySide import QtCore, QtGui, __version__, __version_info__
        import shiboken
        # PySide 1.0.3 fixed the following:
        # https://srinikom.github.io/pyside-bz-archive/809.html
        if __version_info__ < (1, 0, 3):
            raise ImportError("PySide<1.0.3 is not supported")
        def _isdeleted(obj): return not shiboken.isValid(obj)
        _getSaveFileName = QtGui.QFileDialog.getSaveFileName
    elif QT_API == QT_API_PYQT:
        _setup_pyqt4_internal(api=1)
    else:
        raise ValueError("Unexpected value for the 'backend.qt4' rcparam")
    QtWidgets = QtGui

    @_api.deprecated("3.3", alternative="QtCore.qVersion()")
    def is_pyqt5():
        return False
