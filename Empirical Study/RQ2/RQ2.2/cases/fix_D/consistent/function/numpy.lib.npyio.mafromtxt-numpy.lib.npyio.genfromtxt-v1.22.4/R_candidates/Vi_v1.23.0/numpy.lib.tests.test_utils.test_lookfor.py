@pytest.mark.skipif(sys.flags.optimize == 2, reason="Python running -OO")
@pytest.mark.skipif(
    sys.version_info == (3, 10, 0, "candidate", 1),
    reason="Broken as of bpo-44524",
)
def test_lookfor():
    out = StringIO()
    utils.lookfor('eigenvalue', module='numpy', output=out,
                  import_modules=False)
    out = out.getvalue()
    assert_('numpy.linalg.eig' in out)
