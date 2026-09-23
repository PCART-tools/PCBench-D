def test_tensor_life_with_checkpointing():
    skip_layout = SkipLayout(num_partitions=2, skip_routes={(None, "test"): (0, 1)})
    skip_tracker = SkipTrackerThroughPotals(skip_layout)

    batch = Batch(torch.tensor([1.0]))
    tensor = torch.tensor([2.0])

    with enable_checkpointing():
        skip_tracker.save(batch, None, "test", tensor)
    assert skip_tracker.portals[(None, "test")].tensor_life == 2

    with enable_checkpointing():
        skip_tracker.load(batch, None, "test")
    assert skip_tracker.portals[(None, "test")].tensor_life == 1

    with enable_recomputing():
        skip_tracker.load(batch, None, "test")
    assert skip_tracker.portals[(None, "test")].tensor_life == 0

    with enable_recomputing():
        skip_tracker.save(batch, None, "test", tensor)
    assert skip_tracker.portals[(None, "test")].tensor_life == 0
