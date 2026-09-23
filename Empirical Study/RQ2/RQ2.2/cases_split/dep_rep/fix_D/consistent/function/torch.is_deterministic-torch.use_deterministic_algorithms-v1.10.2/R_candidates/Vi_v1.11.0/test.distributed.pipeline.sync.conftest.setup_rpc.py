@pytest.fixture
def setup_rpc(scope="session"):
    file = tempfile.NamedTemporaryFile()
    dist.rpc.init_rpc(
        name="worker0",
        rank=0,
        world_size=1,
        rpc_backend_options=dist.rpc.TensorPipeRpcBackendOptions(
            init_method="file://{}".format(file.name),
        )
    )
    yield
    dist.rpc.shutdown()
