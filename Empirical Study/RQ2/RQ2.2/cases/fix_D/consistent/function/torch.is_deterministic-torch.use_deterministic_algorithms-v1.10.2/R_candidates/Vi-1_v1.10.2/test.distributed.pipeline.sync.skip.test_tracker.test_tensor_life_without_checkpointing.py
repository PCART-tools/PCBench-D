def test_tensor_life_without_checkpointing():
    skip_layout = SkipLayout(num_partitions=2, skip_routes={(None, "test"): (0, 1)})
    skip_tracker = SkipTrackerThroughPotals(skip_layout)

    batch = Batch(torch.tensor([1.0]))
    tensor = torch.tensor([2.0])

    skip_tracker.save(batch, None, "test", tensor)
    assert skip_tracker.portals[(None, "test")].tensor_life == 1

    skip_tracker.load(batch, None, "test")
    assert skip_tracker.portals[(None, "test")].tensor_life == 0
