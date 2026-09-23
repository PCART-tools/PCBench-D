def _setup_pyqt5plus():
    global QtCore, QtGui, QtWidgets, __version__, _isdeleted, _getSaveFileName

    if QT_API == QT_API_PYQT6:
        from PyQt6 import QtCore, QtGui, QtWidgets, sip
        __version__ = QtCore.PYQT_VERSION_STR
        QtCore.Signal = QtCore.pyqtSignal
        QtCore.Slot = QtCore.pyqtSlot
        QtCore.Property = QtCore.pyqtProperty
        _isdeleted = sip.isdeleted
    elif QT_API == QT_API_PYSIDE6:
        from PySide6 import QtCore, QtGui, QtWidgets, __version__
        import shiboken6
        def _isdeleted(obj): return not shiboken6.isValid(obj)
    elif QT_API == QT_API_PYQT5:
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
        def _isdeleted(obj):
            return not shiboken2.isValid(obj)
    else:
        raise AssertionError(f"Unexpected QT_API: {QT_API}")
    _getSaveFileName = QtWidgets.QFileDialog.getSaveFileName
