def test_normalize_kwarg_warn_pie():
    fig, ax = plt.subplots()
    with pytest.warns(MatplotlibDeprecationWarning):
        ax.pie(x=[0], normalize=None)
