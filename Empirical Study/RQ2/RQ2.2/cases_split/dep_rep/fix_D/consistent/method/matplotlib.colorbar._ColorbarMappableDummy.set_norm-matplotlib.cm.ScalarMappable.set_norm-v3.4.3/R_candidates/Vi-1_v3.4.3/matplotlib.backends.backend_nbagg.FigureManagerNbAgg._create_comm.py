    def _create_comm(self):
        comm = CommSocket(self)
        self.add_web_socket(comm)
        return comm
