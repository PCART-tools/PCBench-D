def test_coerce():
    d0 = da.from_array(np.array(1), chunks=(1,))
    d1 = da.from_array(np.array([1]), chunks=(1,))
    with dask.config.set(scheduler='sync'):
        for d in d0, d1:
            assert bool(d) is True
            assert int(d) == 1
            assert float(d) == 1.0
            assert complex(d) == complex(1)

    a2 = np.arange(2)
    d2 = da.from_array(a2, chunks=(2,))
    for func in (int, float, complex):
        pytest.raises(TypeError, lambda :func(d2))
