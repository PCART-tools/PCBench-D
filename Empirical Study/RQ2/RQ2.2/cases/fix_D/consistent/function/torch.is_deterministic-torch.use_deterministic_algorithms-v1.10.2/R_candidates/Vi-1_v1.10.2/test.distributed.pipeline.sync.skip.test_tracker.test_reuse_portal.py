def test_reuse_portal():
    skip_layout = SkipLayout(num_partitions=2, skip_routes={(None, "test"): (0, 1)})
    skip_tracker = SkipTrackerThroughPotals(skip_layout)

    batch = Batch(torch.tensor([1.0]))
    a = torch.tensor([2.0])
    b = torch.tensor([2.0])

    skip_tracker.save(batch, None, "test", a)
    portal = skip_tracker.portals[(None, "test")]

    skip_tracker.save(batch, None, "test", b)
    assert portal is skip_tracker.portals[(None, "test")]
