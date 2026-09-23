    @classmethod
    def get_javascript(cls, stream=None):
        if stream is None:
            output = io.StringIO()
        else:
            output = stream

        with io.open(os.path.join(
                os.path.dirname(__file__),
                "web_backend",
                "mpl.js"), encoding='utf8') as fd:
            output.write(fd.read())

        toolitems = []
        for name, tooltip, image, method in cls.ToolbarCls.toolitems:
            if name is None:
                toolitems.append(['', '', '', ''])
            else:
                toolitems.append([name, tooltip, image, method])
        output.write("mpl.toolbar_items = {0};\n\n".format(
            json.dumps(toolitems)))

        extensions = []
        for filetype, ext in sorted(FigureCanvasWebAggCore.
                                    get_supported_filetypes_grouped().
                                    items()):
            if not ext[0] == 'pgf':  # pgf does not support BytesIO
                extensions.append(ext[0])
        output.write("mpl.extensions = {0};\n\n".format(
            json.dumps(extensions)))

        output.write("mpl.default_extension = {0};".format(
            json.dumps(FigureCanvasWebAggCore.get_default_filetype())))

        if stream is None:
            return output.getvalue()
