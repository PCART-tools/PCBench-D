@pytest.mark.parametrize('myopen,compression',
                         [(open, None), (GzipFile, 'gzip'), (BZ2File, 'bz2'),
                          SKIP_XZ((LZMAFile, 'xz'))])
def test_filesize(myopen, compression):
    text = b'123 456 789 abc def ghi'.replace(b' ', os.linesep.encode())
    with filetext(text, open=myopen, mode='wb') as fn:
        assert file_size(fn, compression) == len(text)
