def replay_shape_env_events(events):
    from torch.fx.experimental.symbolic_shapes import ShapeEnv

    constructor_event = events[0]
    assert constructor_event.f == ShapeEnv

    # Constructs the new ShapeEnv.
    shape_env = constructor_event.run()

    for event in events[1:]:
        try:
            # Actually replays each event.
            # We need to call create_mapping_fn every time, since the node list might
            # change after each event is replayed.
            event.run(shape_env)
        except Exception:
            log.error("failed when running event: %s", event)
            raise

    return shape_env
