@pytest.mark.parametrize('shape, chunks, pad_width, mode, kwargs', [
    ((10,), (3,), 1, 'constant', {}),
    ((10,), (3,), 2, 'constant', {'constant_values': -1}),
    ((10,), (3,), ((2, 3)), 'constant', {'constant_values': (-1, -2)}),
    (
        (10, 11), (4, 5), ((1, 4), (2, 3)), 'constant',
        {'constant_values': ((-1, -2), (2, 1))}
    ),
    ((10,), (3,), 3, 'edge', {}),
    ((10,), (3,), 3, 'linear_ramp', {}),
    ((10,), (3,), 3, 'linear_ramp', {'end_values': 0}),
    ((10, 11), (4, 5), ((1, 4), (2, 3)), 'reflect', {}),
    ((10, 11), (4, 5), ((1, 4), (2, 3)), 'symmetric', {}),
    ((10, 11), (4, 5), ((1, 4), (2, 3)), 'wrap', {}),
    ((10,), (3,), ((2, 3)), 'maximum', {'stat_length': (1, 2)}),
    (
        (10, 11), (4, 5), ((1, 4), (2, 3)), 'mean',
        {'stat_length': ((3, 4), (2, 1))}
    ),
    ((10,), (3,), ((2, 3)), 'minimum', {'stat_length': (2, 3)}),
])
def test_pad(shape, chunks, pad_width, mode, kwargs):
    np_a = np.random.random(shape)
    da_a = da.from_array(np_a, chunks=chunks)

    np_r = np.pad(np_a, pad_width, mode, **kwargs)
    da_r = da.pad(da_a, pad_width, mode, **kwargs)

    assert_eq(np_r, da_r)
