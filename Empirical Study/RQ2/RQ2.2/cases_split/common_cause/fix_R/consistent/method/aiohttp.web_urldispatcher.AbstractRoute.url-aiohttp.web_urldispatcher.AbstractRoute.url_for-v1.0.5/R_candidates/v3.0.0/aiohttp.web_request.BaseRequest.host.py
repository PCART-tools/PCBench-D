    @reify
    def host(self):
        """Hostname of the request.

        Hostname is resolved in this order:

        - overridden value by .clone(host=new_host) call.
        - HOST HTTP header
        - socket.getfqdn() value
        """
        host = self._message.headers.get(hdrs.HOST)
        if host is not None:
            return host
        else:
            return socket.getfqdn()
