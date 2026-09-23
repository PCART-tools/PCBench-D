    def clearup_closed(self):
        """Clear up any closed Comms."""
        self.web_sockets = {socket for socket in self.web_sockets
                            if socket.is_open()}

        if len(self.web_sockets) == 0:
            CloseEvent("close_event", self.canvas)._process()
