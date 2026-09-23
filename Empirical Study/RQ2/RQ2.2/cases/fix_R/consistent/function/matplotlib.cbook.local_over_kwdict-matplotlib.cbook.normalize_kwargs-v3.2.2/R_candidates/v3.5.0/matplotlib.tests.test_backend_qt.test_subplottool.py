@pytest.mark.backend('QtAgg', skip_on_importerror=True)
def test_subplottool():
    fig, ax = plt.subplots()
    with mock.patch("matplotlib.backends.qt_compat._exec", lambda obj: None):
        fig.canvas.manager.toolbar.configure_subplots()
