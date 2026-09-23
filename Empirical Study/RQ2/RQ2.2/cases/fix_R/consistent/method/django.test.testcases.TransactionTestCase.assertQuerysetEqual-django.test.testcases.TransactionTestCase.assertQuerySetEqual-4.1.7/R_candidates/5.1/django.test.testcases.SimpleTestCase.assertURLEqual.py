    def assertURLEqual(self, url1, url2, msg_prefix=""):
        """
        Assert that two URLs are the same, ignoring the order of query string
        parameters except for parameters with the same name.

        For example, /path/?x=1&y=2 is equal to /path/?y=2&x=1, but
        /path/?a=1&a=2 isn't equal to /path/?a=2&a=1.
        """

        def normalize(url):
            """Sort the URL's query string parameters."""
            url = str(url)  # Coerce reverse_lazy() URLs.
            scheme, netloc, path, params, query, fragment = urlparse(url)
            query_parts = sorted(parse_qsl(query))
            return urlunparse(
                (scheme, netloc, path, params, urlencode(query_parts), fragment)
            )

        if msg_prefix:
            msg_prefix += ": "
        self.assertEqual(
            normalize(url1),
            normalize(url2),
            msg_prefix + "Expected '%s' to equal '%s'." % (url1, url2),
        )
