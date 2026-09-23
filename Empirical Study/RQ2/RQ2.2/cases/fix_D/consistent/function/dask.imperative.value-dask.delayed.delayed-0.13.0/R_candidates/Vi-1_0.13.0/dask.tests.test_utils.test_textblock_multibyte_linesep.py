def test_textblock_multibyte_linesep():
    text = b'12 34 56 78'.replace(b' ', b'\r\n')
    with filetext(text, mode='wb') as fn:
        text = [line.encode()
                for line in textblock(fn, 5, 13, linesep='\r\n', buffersize=2)]
        assert text == [line.encode() for line in ('56\r\n', '78')]
