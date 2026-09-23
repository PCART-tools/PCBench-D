    @staticmethod
    def show():
        WebAggApplication.initialize()

        url = "http://127.0.0.1:{port}{prefix}".format(
            port=WebAggApplication.port,
            prefix=WebAggApplication.url_prefix)

        if rcParams['webagg.open_in_browser']:
            import webbrowser
            webbrowser.open(url)
        else:
            print("To view figure, visit {0}".format(url))

        WebAggApplication.start()
