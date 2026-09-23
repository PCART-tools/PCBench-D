def test_rcparams(tmpdir):
    mpl.rc('text', usetex=False)
    mpl.rc('lines', linewidth=22)

    usetex = mpl.rcParams['text.usetex']
    linewidth = mpl.rcParams['lines.linewidth']

    rcpath = Path(tmpdir) / 'test_rcparams.rc'
    rcpath.write_text('lines.linewidth: 33')

    # test context given dictionary
    with mpl.rc_context(rc={'text.usetex': not usetex}):
        assert mpl.rcParams['text.usetex'] == (not usetex)
    assert mpl.rcParams['text.usetex'] == usetex

    # test context given filename (mpl.rc sets linewidth to 33)
    with mpl.rc_context(fname=rcpath):
        assert mpl.rcParams['lines.linewidth'] == 33
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test context given filename and dictionary
    with mpl.rc_context(fname=rcpath, rc={'lines.linewidth': 44}):
        assert mpl.rcParams['lines.linewidth'] == 44
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test context as decorator (and test reusability, by calling func twice)
    @mpl.rc_context({'lines.linewidth': 44})
    def func():
        assert mpl.rcParams['lines.linewidth'] == 44

    func()
    func()

    # test rc_file
    mpl.rc_file(rcpath)
    assert mpl.rcParams['lines.linewidth'] == 33
