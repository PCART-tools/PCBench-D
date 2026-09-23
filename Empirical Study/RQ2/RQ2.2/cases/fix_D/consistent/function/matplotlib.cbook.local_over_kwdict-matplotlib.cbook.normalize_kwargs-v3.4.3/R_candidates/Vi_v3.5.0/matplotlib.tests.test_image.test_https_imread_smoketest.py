@pytest.mark.network
@pytest.mark.flaky
def test_https_imread_smoketest():
    with _api.suppress_matplotlib_deprecation_warning():
        v = mimage.imread('https://matplotlib.org/1.5.0/_static/logo2.png')
