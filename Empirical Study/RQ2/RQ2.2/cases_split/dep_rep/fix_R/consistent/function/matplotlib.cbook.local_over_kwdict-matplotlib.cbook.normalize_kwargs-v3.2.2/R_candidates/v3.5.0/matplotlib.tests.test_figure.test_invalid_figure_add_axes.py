def test_invalid_figure_add_axes():
    fig = plt.figure()
    with pytest.raises(ValueError):
        fig.add_axes((.1, .1, .5, np.nan))

    with pytest.raises(TypeError, match="multiple values for argument 'rect'"):
        fig.add_axes([0, 0, 1, 1], rect=[0, 0, 1, 1])

    _, ax = plt.subplots()
    with pytest.raises(ValueError,
                       match="The Axes must have been created in the present "
                             "figure"):
        fig.add_axes(ax)
