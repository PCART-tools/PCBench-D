def test_annotate_parameter_warn():
    fig, ax = plt.subplots()
    with pytest.warns(MatplotlibDeprecationWarning,
                      match=r"The \'s\' parameter of annotate\(\) "
                             "has been renamed \'text\'"):
        ax.annotate(s='now named text', xy=(0, 1))
