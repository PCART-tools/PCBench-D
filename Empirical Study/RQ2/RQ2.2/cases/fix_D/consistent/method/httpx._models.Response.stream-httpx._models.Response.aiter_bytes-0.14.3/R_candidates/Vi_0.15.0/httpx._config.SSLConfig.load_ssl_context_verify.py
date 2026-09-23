    def load_ssl_context_verify(self) -> ssl.SSLContext:
        """
        Return an SSL context for verified connections.
        """
        if self.trust_env and self.verify is True:
            ca_bundle = get_ca_bundle_from_env()
            if ca_bundle is not None:
                self.verify = ca_bundle

        if isinstance(self.verify, ssl.SSLContext):
            # Allow passing in our own SSLContext object that's pre-configured.
            context = self.verify
            self._load_client_certs(context)
            return context
        elif isinstance(self.verify, bool):
            ca_bundle_path = self.DEFAULT_CA_BUNDLE_PATH
        elif Path(self.verify).exists():
            ca_bundle_path = Path(self.verify)
        else:
            raise IOError(
                "Could not find a suitable TLS CA certificate bundle, "
                "invalid path: {}".format(self.verify)
            )

        context = self._create_default_ssl_context()
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True

        # Signal to server support for PHA in TLS 1.3. Raises an
        # AttributeError if only read-only access is implemented.
        try:
            context.post_handshake_auth = True  # type: ignore
        except AttributeError:  # pragma: nocover
            pass

        # Disable using 'commonName' for SSLContext.check_hostname
        # when the 'subjectAltName' extension isn't available.
        try:
            context.hostname_checks_common_name = False  # type: ignore
        except AttributeError:  # pragma: nocover
            pass

        if ca_bundle_path.is_file():
            logger.trace(f"load_verify_locations cafile={ca_bundle_path!s}")
            context.load_verify_locations(cafile=str(ca_bundle_path))
        elif ca_bundle_path.is_dir():
            logger.trace(f"load_verify_locations capath={ca_bundle_path!s}")
            context.load_verify_locations(capath=str(ca_bundle_path))

        self._load_client_certs(context)

        return context
