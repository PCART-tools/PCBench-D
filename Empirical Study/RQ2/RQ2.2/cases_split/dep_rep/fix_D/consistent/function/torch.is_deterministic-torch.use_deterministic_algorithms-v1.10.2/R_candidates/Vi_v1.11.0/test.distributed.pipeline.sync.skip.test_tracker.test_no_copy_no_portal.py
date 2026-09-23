def test_no_copy_no_portal():
    skip_layout = SkipLayout(num_partitions=2, skip_routes={(None, "copy"): (0, 1), (None, "not_copy"): (0, 0)})
    skip_tracker = SkipTrackerThroughPotals(skip_layout)

    batch = Batch(torch.tensor([1.0]))
    a = torch.tensor([2.0])
    b = torch.tensor([2.0])

    skip_tracker.save(batch, None, "copy", a)
    skip_tracker.save(batch, None, "not_copy", b)

    assert (None, "copy") in skip_tracker.portals
    assert (None, "copy") not in skip_tracker.tensors
    assert (None, "not_copy") in skip_tracker.tensors
    assert (None, "not_copy") not in skip_tracker.portals
