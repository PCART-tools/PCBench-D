def _setup_pyqt5():
    global QtCore, QtGui, QtWidgets, __version__, is_pyqt5, \
        _isdeleted, _getSaveFileName

    if QT_API == QT_API_PYQT5:
        from PyQt5 import QtCore, QtGui, QtWidgets
        import sip
        __version__ = QtCore.PYQT_VERSION_STR
        QtCore.Signal = QtCore.pyqtSignal
        QtCore.Slot = QtCore.pyqtSlot
        QtCore.Property = QtCore.pyqtProperty
        _isdeleted = sip.isdeleted
    elif QT_API == QT_API_PYSIDE2:
        from PySide2 import QtCore, QtGui, QtWidgets, __version__
        import shiboken2
        def _isdeleted(obj): return not shiboken2.isValid(obj)
    else:
        raise ValueError("Unexpected value for the 'backend.qt5' rcparam")
    _getSaveFileName = QtWidgets.QFileDialog.getSaveFileName

    @_api.deprecated("3.3", alternative="QtCore.qVersion()")
    def is_pyqt5():
        return True
