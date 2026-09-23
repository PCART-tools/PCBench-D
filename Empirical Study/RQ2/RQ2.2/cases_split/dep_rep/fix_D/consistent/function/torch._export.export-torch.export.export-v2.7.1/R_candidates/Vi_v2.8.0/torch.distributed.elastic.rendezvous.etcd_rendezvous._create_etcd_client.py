def _create_etcd_client(params: RendezvousParameters) -> etcd.Client:
    """Create a new ``etcd.Client`` from the specified ``RendezvousParameters``."""
    hostname, port = parse_rendezvous_endpoint(params.endpoint, 2379)

    # The communication protocol
    protocol = params.config.get("protocol")
    if protocol is None:
        protocol = "http"
    else:
        if protocol != "http" and protocol != "https":
            raise ValueError("The etcd protocol must be HTTP or HTTPS.")

    # The SSL client certificate
    ssl_cert = params.config.get("cert")
    if ssl_cert is not None:
        cert_key = params.config.get("key")
        if cert_key is not None:
            # The etcd client expects the certificate key as the second element
            # of the `cert` tuple.
            ssl_cert = (ssl_cert, cert_key)

    # The root certificate
    ca_cert = params.config.get("cacert")

    return etcd.Client(
        hostname,
        port,
        protocol=protocol,
        cert=ssl_cert,
        ca_cert=ca_cert,
        allow_reconnect=True,
    )
