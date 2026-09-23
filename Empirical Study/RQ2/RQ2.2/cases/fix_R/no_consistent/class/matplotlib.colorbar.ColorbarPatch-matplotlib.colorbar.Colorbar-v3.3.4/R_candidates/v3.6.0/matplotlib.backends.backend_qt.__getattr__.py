@_api.caching_module_getattr
class __getattr__:
    qApp = _api.deprecated(
        "3.6", alternative="QtWidgets.QApplication.instance()")(
            property(lambda self: QtWidgets.QApplication.instance()))
