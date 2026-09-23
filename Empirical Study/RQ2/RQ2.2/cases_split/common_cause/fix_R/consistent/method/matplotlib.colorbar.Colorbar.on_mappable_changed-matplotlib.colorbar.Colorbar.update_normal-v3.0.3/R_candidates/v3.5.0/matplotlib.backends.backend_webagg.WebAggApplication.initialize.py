    @classmethod
    def initialize(cls, url_prefix='', port=None, address=None):
        if cls.initialized:
            return

        # Create the class instance
        app = cls(url_prefix=url_prefix)

        cls.url_prefix = url_prefix

        # This port selection algorithm is borrowed, more or less
        # verbatim, from IPython.
        def random_ports(port, n):
            """
            Generate a list of n random ports near the given port.

            The first 5 ports will be sequential, and the remaining n-5 will be
            randomly selected in the range [port-2*n, port+2*n].
            """
            for i in range(min(5, n)):
                yield port + i
            for i in range(n - 5):
                yield port + random.randint(-2 * n, 2 * n)

        if address is None:
            cls.address = mpl.rcParams['webagg.address']
        else:
            cls.address = address
        cls.port = mpl.rcParams['webagg.port']
        for port in random_ports(cls.port,
                                 mpl.rcParams['webagg.port_retries']):
            try:
                app.listen(port, cls.address)
            except socket.error as e:
                if e.errno != errno.EADDRINUSE:
                    raise
            else:
                cls.port = port
                break
        else:
            raise SystemExit(
                "The webagg server could not be started because an available "
                "port could not be found")

        cls.initialized = True
