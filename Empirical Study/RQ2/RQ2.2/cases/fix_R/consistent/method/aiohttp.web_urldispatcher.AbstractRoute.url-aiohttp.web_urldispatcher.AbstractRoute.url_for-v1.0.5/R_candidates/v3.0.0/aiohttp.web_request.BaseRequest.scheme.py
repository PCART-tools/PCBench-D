    @reify
    def scheme(self):
        """A string representing the scheme of the request.

        Hostname is resolved in this order:

        - overridden value by .clone(scheme=new_scheme) call.
        - type of connection to peer: HTTPS if socket is SSL, HTTP otherwise.

        'http' or 'https'.
        """
        if self.transport.get_extra_info('sslcontext'):
            return 'https'
        else:
            return 'http'
