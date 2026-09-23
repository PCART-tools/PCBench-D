def _create_c10d_store_mp(is_server, server_addr, port, world_size):
    store = create_c10d_store(is_server, server_addr, port, world_size, timeout=2)
    if store is None:
        raise AssertionError()

    store.set(f"test_key/{os.getpid()}", "test_value".encode("UTF-8"))
