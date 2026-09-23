    @classmethod
    def get_javascript(cls, stream=None):
        if stream is None:
            output = io.StringIO()
        else:
            output = stream
        super(FigureManagerNbAgg, cls).get_javascript(stream=output)
        with io.open(os.path.join(
                os.path.dirname(__file__),
                "web_backend",
                "nbagg_mpl.js"), encoding='utf8') as fd:
            output.write(fd.read())
        if stream is None:
            return output.getvalue()
