    def __init__(
        self,
        *,
        verify: VerifyTypes = True,
        cert: CertTypes = None,
        trust_env: bool = None,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        pool_block: bool = False,
    ):
        assert (
            urllib3 is not None
        ), "urllib3 must be installed in order to use URLLib3Transport"

        self.pool = urllib3.PoolManager(
            ssl_context=create_ssl_context(
                verify=verify, cert=cert, trust_env=trust_env, http2=False
            ),
            num_pools=pool_connections,
            maxsize=pool_maxsize,
            block=pool_block,
        )
