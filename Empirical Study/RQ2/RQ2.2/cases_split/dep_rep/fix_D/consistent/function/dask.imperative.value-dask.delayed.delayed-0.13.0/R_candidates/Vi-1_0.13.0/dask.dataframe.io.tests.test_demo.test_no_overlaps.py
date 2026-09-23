def test_no_overlaps():
    df = dd.demo.make_timeseries('2000', '2001', {'A': float},
                                 freq='3H', partition_freq='3M')

    assert all(df.get_partition(i).index.max().compute() <
               df.get_partition(i + 1).index.min().compute()
               for i in range(df.npartitions - 2))
