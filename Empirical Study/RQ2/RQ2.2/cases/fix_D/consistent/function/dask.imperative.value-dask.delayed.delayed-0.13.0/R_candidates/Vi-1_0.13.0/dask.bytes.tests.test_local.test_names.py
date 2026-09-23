@pytest.mark.slow
def test_names():
    with filetexts(files, mode='b'):
        _, a = read_bytes('.test.accounts.*')
        _, b = read_bytes('.test.accounts.*')
        a = list(concat(a))
        b = list(concat(b))

        assert [aa._key for aa in a] == [bb._key for bb in b]

        sleep(1)
        for fn in files:
            with open(fn, 'ab') as f:
                f.write(b'x')

        _, c = read_bytes('.test.accounts.*')
        c = list(concat(c))
        assert [aa._key for aa in a] != [cc._key for cc in c]
