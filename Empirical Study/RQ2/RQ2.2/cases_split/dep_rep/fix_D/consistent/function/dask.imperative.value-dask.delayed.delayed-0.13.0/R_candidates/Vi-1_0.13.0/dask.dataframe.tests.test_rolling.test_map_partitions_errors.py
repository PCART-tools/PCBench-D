def test_map_partitions_errors():
    # Non-integer
    with pytest.raises(ValueError):
        ddf.map_overlap(shifted_sum, 0.5, 3, 0, 2, c=2)

    # Negative
    with pytest.raises(ValueError):
        ddf.map_overlap(shifted_sum, 0, -5, 0, 2, c=2)

    # Partition size < window size
    with pytest.raises(NotImplementedError):
        ddf.map_overlap(shifted_sum, 0, 100, 0, 100, c=2).compute()
