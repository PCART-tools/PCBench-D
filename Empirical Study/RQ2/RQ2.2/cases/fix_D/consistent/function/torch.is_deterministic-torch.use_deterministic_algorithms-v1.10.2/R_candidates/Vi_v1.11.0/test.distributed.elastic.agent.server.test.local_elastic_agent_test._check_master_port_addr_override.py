def _check_master_port_addr_override(
    expected_master_addr: str, expected_master_port: int
):
    actual_master_addr = os.environ["MASTER_ADDR"]
    actual_master_port = int(os.environ["MASTER_PORT"])
    if (
        expected_master_addr != actual_master_addr
        and expected_master_port != actual_master_port
    ):
        raise RuntimeError(
            f"Expected addr: {expected_master_addr}:{expected_master_port}, got addr: {actual_master_addr}:{actual_master_port}"
        )
