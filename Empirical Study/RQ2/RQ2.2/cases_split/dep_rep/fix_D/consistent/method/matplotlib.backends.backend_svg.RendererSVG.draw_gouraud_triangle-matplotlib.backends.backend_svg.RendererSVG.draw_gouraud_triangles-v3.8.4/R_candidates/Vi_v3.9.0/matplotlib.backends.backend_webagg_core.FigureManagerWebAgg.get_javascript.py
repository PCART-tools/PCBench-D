    @classmethod
    def get_javascript(cls, stream=None):
        if stream is None:
            output = StringIO()
        else:
            output = stream

        output.write((Path(__file__).parent / "web_backend/js/mpl.js")
                     .read_text(encoding="utf-8"))

        toolitems = []
        for name, tooltip, image, method in cls.ToolbarCls.toolitems:
            if name is None:
                toolitems.append(['', '', '', ''])
            else:
                toolitems.append([name, tooltip, image, method])
        output.write(f"mpl.toolbar_items = {json.dumps(toolitems)};\n\n")

        extensions = []
        for filetype, ext in sorted(FigureCanvasWebAggCore.
                                    get_supported_filetypes_grouped().
                                    items()):
            extensions.append(ext[0])
        output.write(f"mpl.extensions = {json.dumps(extensions)};\n\n")

        output.write("mpl.default_extension = {};".format(
            json.dumps(FigureCanvasWebAggCore.get_default_filetype())))

        if stream is None:
            return output.getvalue()
