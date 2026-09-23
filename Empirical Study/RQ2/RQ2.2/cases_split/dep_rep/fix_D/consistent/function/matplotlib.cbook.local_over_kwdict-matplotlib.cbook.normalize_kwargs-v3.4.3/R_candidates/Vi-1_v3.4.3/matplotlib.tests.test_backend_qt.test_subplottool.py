@pytest.mark.backend('Qt5Agg', skip_on_importerror=True)
def test_subplottool():
    fig, ax = plt.subplots()
    with mock.patch(
            "matplotlib.backends.backend_qt5.SubplotToolQt.exec_",
            lambda self: None):
        fig.canvas.manager.toolbar.configure_subplots()
