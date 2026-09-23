def _refresh_packet(packet):
    op, overload_names = _get_packet(packet._qualified_op_name, packet._op.__module__)
    assert op is not None
    packet._op = op
    packet._overload_names = overload_names
