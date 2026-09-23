@pytest.mark.parametrize(["dtype", "value"], [
        ("i2", 0x0001), ("u2", 0x0001),
        ("i4", 0x00010203), ("u4", 0x00010203),
        ("i8", 0x0001020304050607), ("u8", 0x0001020304050607),
        # The following values are constructed to lead to unique bytes:
        ("float16", 3.07e-05),
        ("float32", 9.2557e-41), ("complex64", 9.2557e-41+2.8622554e-29j),
        ("float64", -1.758571353180402e-24),
        # Here and below, the repr side-steps a small loss of precision in
        # complex `str` in PyPy (which is probably fine, as repr works):
        ("complex128", repr(5.406409232372729e-29-1.758571353180402e-24j)),
        # Use integer values that fit into double.  Everything else leads to
        # problems due to longdoubles going via double and decimal strings
        # causing rounding errors.
        ("longdouble", 0x01020304050607),
        ("clongdouble", repr(0x01020304050607 + (0x00121314151617 * 1j))),
        ("U2", "\U00010203\U000a0b0c")])
@pytest.mark.parametrize("swap", [True, False])
def test_byteswapping_and_unaligned(dtype, value, swap):
    # Try to create "interesting" values within the valid unicode range:
    dtype = np.dtype(dtype)
    data = [f"x,{value}\n"]  # repr as PyPy `str` truncates some
    if swap:
        dtype = dtype.newbyteorder()
    full_dt = np.dtype([("a", "S1"), ("b", dtype)], align=False)
    # The above ensures that the interesting "b" field is unaligned:
    assert full_dt.fields["b"][1] == 1
    res = np.loadtxt(data, dtype=full_dt, delimiter=",", encoding=None,
                     max_rows=1)  # max-rows prevents over-allocation
    assert res["b"] == dtype.type(value)
