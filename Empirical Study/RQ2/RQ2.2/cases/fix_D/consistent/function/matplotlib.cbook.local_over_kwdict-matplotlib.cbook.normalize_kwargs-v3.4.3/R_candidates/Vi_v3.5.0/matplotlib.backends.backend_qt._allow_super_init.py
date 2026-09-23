def _allow_super_init(__init__):
    """
    Decorator for ``__init__`` to allow ``super().__init__`` on PySide2.
    """

    if QT_API in ["PyQt5", "PyQt6"]:

        return __init__

    else:
        # To work around lack of cooperative inheritance in PySide2 and
        # PySide6, when calling FigureCanvasQT.__init__, we temporarily patch
        # QWidget.__init__ by a cooperative version, that first calls
        # QWidget.__init__ with no additional arguments, and then finds the
        # next class in the MRO with an __init__ that does support cooperative
        # inheritance (i.e., not defined by the PyQt4 or sip, or PySide{,2,6}
        # or Shiboken packages), and manually call its `__init__`, once again
        # passing the additional arguments.

        qwidget_init = QtWidgets.QWidget.__init__

        def cooperative_qwidget_init(self, *args, **kwargs):
            qwidget_init(self)
            mro = type(self).__mro__
            next_coop_init = next(
                cls for cls in mro[mro.index(QtWidgets.QWidget) + 1:]
                if cls.__module__.split(".")[0] not in [
                    "PySide2", "PySide6", "Shiboken",
                ])
            next_coop_init.__init__(self, *args, **kwargs)

        @functools.wraps(__init__)
        def wrapper(self, *args, **kwargs):
            with cbook._setattr_cm(QtWidgets.QWidget,
                                   __init__=cooperative_qwidget_init):
                __init__(self, *args, **kwargs)

        return wrapper
