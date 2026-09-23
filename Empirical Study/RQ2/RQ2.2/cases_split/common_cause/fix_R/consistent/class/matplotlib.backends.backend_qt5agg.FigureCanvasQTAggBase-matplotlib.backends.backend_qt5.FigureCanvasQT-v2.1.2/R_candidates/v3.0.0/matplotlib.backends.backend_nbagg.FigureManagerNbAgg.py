class FigureManagerNbAgg(FigureManagerWebAgg):
    ToolbarCls = NavigationIPy

    def __init__(self, canvas, num):
        self._shown = False
        FigureManagerWebAgg.__init__(self, canvas, num)

    def display_js(self):
        # XXX How to do this just once? It has to deal with multiple
        # browser instances using the same kernel (require.js - but the
        # file isn't static?).
        display(Javascript(FigureManagerNbAgg.get_javascript()))

    def show(self):
        if not self._shown:
            self.display_js()
            self._create_comm()
        else:
            self.canvas.draw_idle()
        self._shown = True

    def reshow(self):
        """
        A special method to re-show the figure in the notebook.

        """
        self._shown = False
        self.show()

    @property
    def connected(self):
        return bool(self.web_sockets)

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

    def _create_comm(self):
        comm = CommSocket(self)
        self.add_web_socket(comm)
        return comm

    def destroy(self):
        self._send_event('close')
        # need to copy comms as callbacks will modify this list
        for comm in list(self.web_sockets):
            comm.on_close()
        self.clearup_closed()

    def clearup_closed(self):
        """Clear up any closed Comms."""
        self.web_sockets = {socket for socket in self.web_sockets
                            if socket.is_open()}

        if len(self.web_sockets) == 0:
            self.canvas.close_event()

    def remove_comm(self, comm_id):
        self.web_sockets = {socket for socket in self.web_sockets
                            if not socket.comm.comm_id == comm_id}
