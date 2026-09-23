def test_gh606():
    encoding = 'utf-16-le'
    euro = u'\u20ac'
    yen = u'\u00a5'
    linesep = os.linesep

    bin_euro = u'\u20ac'.encode(encoding)
    bin_linesep = linesep.encode(encoding)

    data = (euro * 10) + linesep + (yen * 10) + linesep + (euro * 10)
    bin_data = data.encode(encoding)

    with tmpfile() as fn:
        with open(fn, 'wb') as f:
            f.write(bin_data)

        stop = len(bin_euro) * 10 + len(bin_linesep) + 1
        res = ''.join(textblock(fn, 1, stop, encoding=encoding)).encode(encoding)
        assert res == ((yen * 10) + linesep).encode(encoding)

        stop = len(bin_euro) * 10 + len(bin_linesep) + 1
        res = ''.join(textblock(fn, 0, stop, encoding=encoding)).encode(encoding)
        assert res == ((euro * 10) + linesep + (yen * 10) + linesep).encode(encoding)
