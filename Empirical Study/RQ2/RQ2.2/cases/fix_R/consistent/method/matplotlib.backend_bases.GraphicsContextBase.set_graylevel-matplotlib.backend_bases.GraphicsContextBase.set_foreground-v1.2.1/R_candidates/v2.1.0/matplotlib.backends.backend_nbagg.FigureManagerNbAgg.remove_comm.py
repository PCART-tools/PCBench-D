    def remove_comm(self, comm_id):
        self.web_sockets = set([socket for socket in self.web_sockets
                                if not socket.comm.comm_id == comm_id])
