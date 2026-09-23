def test_savefig_warns():
    fig = plt.figure()
    msg = r'savefig\(\) got unexpected keyword argument "non_existent_kwarg"'
    for format in ['png', 'pdf', 'svg', 'tif', 'jpg']:
        with pytest.warns(cbook.MatplotlibDeprecationWarning, match=msg):
            fig.savefig(io.BytesIO(), format=format, non_existent_kwarg=True)
