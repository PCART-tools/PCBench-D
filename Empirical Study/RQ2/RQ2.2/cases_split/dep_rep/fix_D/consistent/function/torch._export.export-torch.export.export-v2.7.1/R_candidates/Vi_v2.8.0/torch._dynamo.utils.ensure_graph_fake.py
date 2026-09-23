def ensure_graph_fake(e, tx):
    assert maybe_get_fake_mode(e) is tx.fake_mode
    return e
