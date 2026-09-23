@pytest.mark.parametrize('kwargs', [
    {},
    {"scaler": 2},
])
def test_pad_udf(kwargs):
    def udf_pad(vector, pad_width, iaxis, kwargs):
        scaler = kwargs.get("scaler", 1)
        vector[:pad_width[0]] = -scaler * pad_width[0]
        vector[-pad_width[1]:] = scaler * pad_width[1]
        return vector

    shape = (10, 11)
    chunks = (4, 5)
    pad_width = ((1, 2), (2, 3))

    np_a = np.random.random(shape)
    da_a = da.from_array(np_a, chunks=chunks)

    np_r = np.pad(np_a, pad_width, udf_pad, kwargs=kwargs)
    da_r = da.pad(da_a, pad_width, udf_pad, kwargs=kwargs)

    assert_eq(np_r, da_r)
