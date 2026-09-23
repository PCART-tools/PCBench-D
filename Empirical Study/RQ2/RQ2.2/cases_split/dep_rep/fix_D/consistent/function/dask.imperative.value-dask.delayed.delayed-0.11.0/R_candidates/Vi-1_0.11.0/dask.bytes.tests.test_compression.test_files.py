@pytest.mark.parametrize('fmt,File', files.items())
def test_files(fmt,File):
    if fmt is None:
        return
    data = b'1234'*1000
    out = BytesIO()
    f = File(out, mode='wb')
    f.write(data)
    f.close()

    out.seek(0)
    compressed = out.read()

    assert len(data) > len(compressed)

    b = BytesIO(compressed)
    g = File(b, mode='rb')
    data2 = g.read()
    g.close()
    assert data == data2
