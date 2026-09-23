    @classmethod
    def get_javascript(cls, stream=None):
        if stream is None:
            output = io.StringIO()
        else:
            output = stream
        super().get_javascript(stream=output)
        output.write((pathlib.Path(__file__).parent
                      / "web_backend/js/nbagg_mpl.js")
                     .read_text(encoding="utf-8"))
        if stream is None:
            return output.getvalue()
