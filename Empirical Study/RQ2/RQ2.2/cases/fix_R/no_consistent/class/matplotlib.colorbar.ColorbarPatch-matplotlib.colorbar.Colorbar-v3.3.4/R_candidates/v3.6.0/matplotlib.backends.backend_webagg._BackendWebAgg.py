@_Backend.export
class _BackendWebAgg(_Backend):
    FigureCanvas = FigureCanvasWebAgg
    FigureManager = FigureManagerWebAgg

    @staticmethod
    def show(*, block=None):
        WebAggApplication.initialize()

        url = "http://{address}:{port}{prefix}".format(
            address=WebAggApplication.address,
            port=WebAggApplication.port,
            prefix=WebAggApplication.url_prefix)

        if mpl.rcParams['webagg.open_in_browser']:
            import webbrowser
            if not webbrowser.open(url):
                print("To view figure, visit {0}".format(url))
        else:
            print("To view figure, visit {0}".format(url))

        WebAggApplication.start()
