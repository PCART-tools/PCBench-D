@pytest.mark.parametrize('open_files', [open_files, open_text_files])
def test_modification_time_open_files(open_files):
    with filetexts(files, mode='b'):
        a = open_files('.test.accounts.*')
        b = open_files('.test.accounts.*')

        assert [aa._key for aa in a] == [bb._key for bb in b]

    sleep(1)

    double = lambda x: x + x
    with filetexts(valmap(double, files), mode='b'):
        c = open_files('.test.accounts.*')

    assert [aa._key for aa in a] != [cc._key for cc in c]
