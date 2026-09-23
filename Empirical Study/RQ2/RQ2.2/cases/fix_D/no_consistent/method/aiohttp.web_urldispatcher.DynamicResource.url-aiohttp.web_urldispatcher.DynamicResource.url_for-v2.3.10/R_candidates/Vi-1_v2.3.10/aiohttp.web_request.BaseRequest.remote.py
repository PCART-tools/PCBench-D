    @reify
    def remote(self):
        """Remote IP of client initiated HTTP request.

        The IP is resolved in this order:

        - overridden value by .clone(remote=new_remote) call.
        - peername of opened socket
        """
        remote = self._remote
        if remote is not None:
            return remote
        transport = self._transport
        peername = transport.get_extra_info('peername')
        if isinstance(peername, (list, tuple)):
            return peername[0]
        else:
            return peername
