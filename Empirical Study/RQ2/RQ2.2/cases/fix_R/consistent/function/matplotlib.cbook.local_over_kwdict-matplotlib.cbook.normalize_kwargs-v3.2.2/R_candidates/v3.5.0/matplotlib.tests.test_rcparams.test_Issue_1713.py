def test_Issue_1713(tmpdir):
    rcpath = Path(tmpdir) / 'test_rcparams.rc'
    rcpath.write_text('timezone: UTC', encoding='UTF-32-BE')
    with mock.patch('locale.getpreferredencoding', return_value='UTF-32-BE'):
        rc = mpl.rc_params_from_file(rcpath, True, False)
    assert rc.get('timezone') == 'UTC'
