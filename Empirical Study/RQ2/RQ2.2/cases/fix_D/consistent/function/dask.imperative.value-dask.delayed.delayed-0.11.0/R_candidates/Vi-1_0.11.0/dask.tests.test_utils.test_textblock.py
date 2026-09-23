@pytest.mark.parametrize('myopen,compression',
                         [(open, None), (GzipFile, 'gzip'), (BZ2File, 'bz2'),
                          SKIP_XZ((LZMAFile, 'xz'))])
def test_textblock(myopen, compression):
    text = b'123 456 789 abc def ghi'.replace(b' ', os.linesep.encode())
    with filetext(text, open=myopen, mode='wb') as fn:
        text = ''.join(textblock(fn, 1, 11, compression)).encode()
        assert text == ('456 789 '.replace(' ', os.linesep)).encode()
        assert set(map(len, text.split())) == set([3])

        k = 3 + len(os.linesep)
        assert ''.join(textblock(fn, 0, k, compression)).encode() == ('123' + os.linesep).encode()
        assert ''.join(textblock(fn, k, k, compression)).encode() == b''
