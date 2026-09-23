    def destroy(self):
        self._send_event('close')
        # need to copy comms as callbacks will modify this list
        for comm in list(self.web_sockets):
            comm.on_close()
        self.clearup_closed()
