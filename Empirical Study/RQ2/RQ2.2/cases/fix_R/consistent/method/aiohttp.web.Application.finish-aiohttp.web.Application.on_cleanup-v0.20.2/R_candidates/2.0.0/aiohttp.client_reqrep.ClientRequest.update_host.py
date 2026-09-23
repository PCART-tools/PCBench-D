    def update_host(self, url):
        """Update destination host, port and connection type (ssl)."""
        # get host/port
        if not url.host:
            raise ValueError(
                "Could not parse hostname from URL '{}'".format(url))

        # basic auth info
        username, password = url.user, url.password
        if username:
            self.auth = helpers.BasicAuth(username, password or '')

        # Record entire netloc for usage in host header

        scheme = url.scheme
        self.ssl = scheme in ('https', 'wss')
