class FigureManagerWebAgg(backend_bases.FigureManagerBase):
    ToolbarCls = NavigationToolbar2WebAgg

    def __init__(self, canvas, num):
        self.web_sockets = set()
        super().__init__(canvas, num)
        self.toolbar = self._get_toolbar(canvas)

    def show(self):
        pass

    def _get_toolbar(self, canvas):
        toolbar = self.ToolbarCls(canvas)
        return toolbar

    def resize(self, w, h, forward=True):
        self._send_event(
            'resize',
            size=(w / self.canvas.device_pixel_ratio,
                  h / self.canvas.device_pixel_ratio),
            forward=forward)

    def set_window_title(self, title):
        self._send_event('figure_label', label=title)

    # The following methods are specific to FigureManagerWebAgg

    def add_web_socket(self, web_socket):
        assert hasattr(web_socket, 'send_binary')
        assert hasattr(web_socket, 'send_json')
        self.web_sockets.add(web_socket)
        self.resize(*self.canvas.figure.bbox.size)
        self._send_event('refresh')

    def remove_web_socket(self, web_socket):
        self.web_sockets.remove(web_socket)

    def handle_json(self, content):
        self.canvas.handle_event(content)

    def refresh_all(self):
        if self.web_sockets:
            diff = self.canvas.get_diff_image()
            if diff is not None:
                for s in self.web_sockets:
                    s.send_binary(diff)

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
        output.write("mpl.toolbar_items = {0};\n\n".format(
            json.dumps(toolitems)))

        extensions = []
        for filetype, ext in sorted(FigureCanvasWebAggCore.
                                    get_supported_filetypes_grouped().
                                    items()):
            extensions.append(ext[0])
        output.write("mpl.extensions = {0};\n\n".format(
            json.dumps(extensions)))

        output.write("mpl.default_extension = {0};".format(
            json.dumps(FigureCanvasWebAggCore.get_default_filetype())))

        if stream is None:
            return output.getvalue()

    @classmethod
    def get_static_file_path(cls):
        return os.path.join(os.path.dirname(__file__), 'web_backend')

    def _send_event(self, event_type, **kwargs):
        payload = {'type': event_type, **kwargs}
        for s in self.web_sockets:
            s.send_json(payload)
