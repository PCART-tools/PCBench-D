class TestScatter:
    @image_comparison(['scatter'], style='mpl20', remove_text=True)
    def test_scatter_plot(self):
        data = {"x": np.array([3, 4, 2, 6]), "y": np.array([2, 5, 2, 3]),
                "c": ['r', 'y', 'b', 'lime'], "s": [24, 15, 19, 29],
                "c2": ['0.5', '0.6', '0.7', '0.8']}

        fig, ax = plt.subplots()
        ax.scatter(data["x"] - 1., data["y"] - 1., c=data["c"], s=data["s"])
        ax.scatter(data["x"] + 1., data["y"] + 1., c=data["c2"], s=data["s"])
        ax.scatter("x", "y", c="c", s="s", data=data)

    @image_comparison(['scatter_marker.png'], remove_text=True)
    def test_scatter_marker(self):
        fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)
        ax0.scatter([3, 4, 2, 6], [2, 5, 2, 3],
                    c=[(1, 0, 0), 'y', 'b', 'lime'],
                    s=[60, 50, 40, 30],
                    edgecolors=['k', 'r', 'g', 'b'],
                    marker='s')
        ax1.scatter([3, 4, 2, 6], [2, 5, 2, 3],
                    c=[(1, 0, 0), 'y', 'b', 'lime'],
                    s=[60, 50, 40, 30],
                    edgecolors=['k', 'r', 'g', 'b'],
                    marker=mmarkers.MarkerStyle('o', fillstyle='top'))
        # unit area ellipse
        rx, ry = 3, 1
        area = rx * ry * np.pi
        theta = np.linspace(0, 2 * np.pi, 21)
        verts = np.column_stack([np.cos(theta) * rx / area,
                                 np.sin(theta) * ry / area])
        ax2.scatter([3, 4, 2, 6], [2, 5, 2, 3],
                    c=[(1, 0, 0), 'y', 'b', 'lime'],
                    s=[60, 50, 40, 30],
                    edgecolors=['k', 'r', 'g', 'b'],
                    marker=verts)

    @image_comparison(['scatter_2D'], remove_text=True, extensions=['png'])
    def test_scatter_2D(self):
        x = np.arange(3)
        y = np.arange(2)
        x, y = np.meshgrid(x, y)
        z = x + y
        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=200, edgecolors='face')

    @check_figures_equal(extensions=["png"])
    def test_scatter_decimal(self, fig_test, fig_ref):
        x0 = np.array([1.5, 8.4, 5.3, 4.2])
        y0 = np.array([1.1, 2.2, 3.3, 4.4])
        x = np.array([Decimal(i) for i in x0])
        y = np.array([Decimal(i) for i in y0])
        c = ['r', 'y', 'b', 'lime']
        s = [24, 15, 19, 29]
        # Test image - scatter plot with Decimal() input
        ax = fig_test.subplots()
        ax.scatter(x, y, c=c, s=s)
        # Reference image
        ax = fig_ref.subplots()
        ax.scatter(x0, y0, c=c, s=s)

    def test_scatter_color(self):
        # Try to catch cases where 'c' kwarg should have been used.
        with pytest.raises(ValueError):
            plt.scatter([1, 2], [1, 2], color=[0.1, 0.2])
        with pytest.raises(ValueError):
            plt.scatter([1, 2, 3], [1, 2, 3], color=[1, 2, 3])

    @pytest.mark.parametrize('kwargs',
                                [
                                    {'cmap': 'gray'},
                                    {'norm': mcolors.Normalize()},
                                    {'vmin': 0},
                                    {'vmax': 0}
                                ])
    def test_scatter_color_warning(self, kwargs):
        warn_match = "No data for colormapping provided "
        # Warn for cases where 'cmap', 'norm', 'vmin', 'vmax'
        # kwargs are being overridden
        with pytest.warns(Warning, match=warn_match):
            plt.scatter([], [], **kwargs)
        with pytest.warns(Warning, match=warn_match):
            plt.scatter([1, 2], [3, 4], c=[], **kwargs)
        # Do not warn for cases where 'c' matches 'x' and 'y'
        plt.scatter([], [], c=[], **kwargs)
        plt.scatter([1, 2], [3, 4], c=[4, 5], **kwargs)

    def test_scatter_unfilled(self):
        coll = plt.scatter([0, 1, 2], [1, 3, 2], c=['0.1', '0.3', '0.5'],
                           marker=mmarkers.MarkerStyle('o', fillstyle='none'),
                           linewidths=[1.1, 1.2, 1.3])
        assert coll.get_facecolors().shape == (0, 4)  # no facecolors
        assert_array_equal(coll.get_edgecolors(), [[0.1, 0.1, 0.1, 1],
                                                   [0.3, 0.3, 0.3, 1],
                                                   [0.5, 0.5, 0.5, 1]])
        assert_array_equal(coll.get_linewidths(), [1.1, 1.2, 1.3])

    @mpl.style.context('default')
    def test_scatter_unfillable(self):
        coll = plt.scatter([0, 1, 2], [1, 3, 2], c=['0.1', '0.3', '0.5'],
                           marker='x',
                           linewidths=[1.1, 1.2, 1.3])
        assert_array_equal(coll.get_facecolors(), coll.get_edgecolors())
        assert_array_equal(coll.get_edgecolors(), [[0.1, 0.1, 0.1, 1],
                                                   [0.3, 0.3, 0.3, 1],
                                                   [0.5, 0.5, 0.5, 1]])
        assert_array_equal(coll.get_linewidths(), [1.1, 1.2, 1.3])

    def test_scatter_size_arg_size(self):
        x = np.arange(4)
        with pytest.raises(ValueError, match='same size as x and y'):
            plt.scatter(x, x, x[1:])
        with pytest.raises(ValueError, match='same size as x and y'):
            plt.scatter(x[1:], x[1:], x)
        with pytest.raises(ValueError, match='float array-like'):
            plt.scatter(x, x, 'foo')

    def test_scatter_edgecolor_RGB(self):
        # GitHub issue 19066
        coll = plt.scatter([1, 2, 3], [1, np.nan, np.nan],
                            edgecolor=(1, 0, 0))
        assert mcolors.same_color(coll.get_edgecolor(), (1, 0, 0))
        coll = plt.scatter([1, 2, 3, 4], [1, np.nan, np.nan, 1],
                            edgecolor=(1, 0, 0, 1))
        assert mcolors.same_color(coll.get_edgecolor(), (1, 0, 0, 1))

    @check_figures_equal(extensions=["png"])
    def test_scatter_invalid_color(self, fig_test, fig_ref):
        ax = fig_test.subplots()
        cmap = mpl.colormaps["viridis"].resampled(16)
        cmap.set_bad("k", 1)
        # Set a nonuniform size to prevent the last call to `scatter` (plotting
        # the invalid points separately in fig_ref) from using the marker
        # stamping fast path, which would result in slightly offset markers.
        ax.scatter(range(4), range(4),
                   c=[1, np.nan, 2, np.nan], s=[1, 2, 3, 4],
                   cmap=cmap, plotnonfinite=True)
        ax = fig_ref.subplots()
        cmap = mpl.colormaps["viridis"].resampled(16)
        ax.scatter([0, 2], [0, 2], c=[1, 2], s=[1, 3], cmap=cmap)
        ax.scatter([1, 3], [1, 3], s=[2, 4], color="k")

    @check_figures_equal(extensions=["png"])
    def test_scatter_no_invalid_color(self, fig_test, fig_ref):
        # With plotnonfinite=False we plot only 2 points.
        ax = fig_test.subplots()
        cmap = mpl.colormaps["viridis"].resampled(16)
        cmap.set_bad("k", 1)
        ax.scatter(range(4), range(4),
                   c=[1, np.nan, 2, np.nan], s=[1, 2, 3, 4],
                   cmap=cmap, plotnonfinite=False)
        ax = fig_ref.subplots()
        ax.scatter([0, 2], [0, 2], c=[1, 2], s=[1, 3], cmap=cmap)

    def test_scatter_norm_vminvmax(self):
        """Parameters vmin, vmax should error if norm is given."""
        x = [1, 2, 3]
        ax = plt.axes()
        with pytest.raises(ValueError,
                           match="Passing a Normalize instance simultaneously "
                                 "with vmin/vmax is not supported."):
            ax.scatter(x, x, c=x, norm=mcolors.Normalize(-10, 10),
                       vmin=0, vmax=5)

    @check_figures_equal(extensions=["png"])
    def test_scatter_single_point(self, fig_test, fig_ref):
        ax = fig_test.subplots()
        ax.scatter(1, 1, c=1)
        ax = fig_ref.subplots()
        ax.scatter([1], [1], c=[1])

    @check_figures_equal(extensions=["png"])
    def test_scatter_different_shapes(self, fig_test, fig_ref):
        x = np.arange(10)
        ax = fig_test.subplots()
        ax.scatter(x, x.reshape(2, 5), c=x.reshape(5, 2))
        ax = fig_ref.subplots()
        ax.scatter(x.reshape(5, 2), x, c=x.reshape(2, 5))

    # Parameters for *test_scatter_c*. NB: assuming that the
    # scatter plot will have 4 elements. The tuple scheme is:
    # (*c* parameter case, exception regexp key or None if no exception)
    params_test_scatter_c = [
        # single string:
        ('0.5', None),
        # Single letter-sequences
        (["rgby"], "conversion"),
        # Special cases
        ("red", None),
        ("none", None),
        (None, None),
        (["r", "g", "b", "none"], None),
        # Non-valid color spec (FWIW, 'jaune' means yellow in French)
        ("jaune", "conversion"),
        (["jaune"], "conversion"),  # wrong type before wrong size
        (["jaune"]*4, "conversion"),
        # Value-mapping like
        ([0.5]*3, None),  # should emit a warning for user's eyes though
        ([0.5]*4, None),  # NB: no warning as matching size allows mapping
        ([0.5]*5, "shape"),
        # list of strings:
        (['0.5', '0.4', '0.6', '0.7'], None),
        (['0.5', 'red', '0.6', 'C5'], None),
        (['0.5', 0.5, '0.6', 'C5'], "conversion"),
        # RGB values
        ([[1, 0, 0]], None),
        ([[1, 0, 0]]*3, "shape"),
        ([[1, 0, 0]]*4, None),
        ([[1, 0, 0]]*5, "shape"),
        # RGBA values
        ([[1, 0, 0, 0.5]], None),
        ([[1, 0, 0, 0.5]]*3, "shape"),
        ([[1, 0, 0, 0.5]]*4, None),
        ([[1, 0, 0, 0.5]]*5, "shape"),
        # Mix of valid color specs
        ([[1, 0, 0, 0.5]]*3 + [[1, 0, 0]], None),
        ([[1, 0, 0, 0.5], "red", "0.0"], "shape"),
        ([[1, 0, 0, 0.5], "red", "0.0", "C5"], None),
        ([[1, 0, 0, 0.5], "red", "0.0", "C5", [0, 1, 0]], "shape"),
        # Mix of valid and non valid color specs
        ([[1, 0, 0, 0.5], "red", "jaune"], "conversion"),
        ([[1, 0, 0, 0.5], "red", "0.0", "jaune"], "conversion"),
        ([[1, 0, 0, 0.5], "red", "0.0", "C5", "jaune"], "conversion"),
    ]

    @pytest.mark.parametrize('c_case, re_key', params_test_scatter_c)
    def test_scatter_c(self, c_case, re_key):
        def get_next_color():
            return 'blue'  # currently unused

        xsize = 4
        # Additional checking of *c* (introduced in #11383).
        REGEXP = {
            "shape": "^'c' argument has [0-9]+ elements",  # shape mismatch
            "conversion": "^'c' argument must be a color",  # bad vals
            }

        if re_key is None:
            mpl.axes.Axes._parse_scatter_color_args(
                c=c_case, edgecolors="black", kwargs={}, xsize=xsize,
                get_next_color_func=get_next_color)
        else:
            with pytest.raises(ValueError, match=REGEXP[re_key]):
                mpl.axes.Axes._parse_scatter_color_args(
                    c=c_case, edgecolors="black", kwargs={}, xsize=xsize,
                    get_next_color_func=get_next_color)

    @mpl.style.context('default')
    @check_figures_equal(extensions=["png"])
    def test_scatter_single_color_c(self, fig_test, fig_ref):
        rgb = [[1, 0.5, 0.05]]
        rgba = [[1, 0.5, 0.05, .5]]

        # set via color kwarg
        ax_ref = fig_ref.subplots()
        ax_ref.scatter(np.ones(3), range(3), color=rgb)
        ax_ref.scatter(np.ones(4)*2, range(4), color=rgba)

        # set via broadcasting via c
        ax_test = fig_test.subplots()
        ax_test.scatter(np.ones(3), range(3), c=rgb)
        ax_test.scatter(np.ones(4)*2, range(4), c=rgba)

    def test_scatter_linewidths(self):
        x = np.arange(5)

        fig, ax = plt.subplots()
        for i in range(3):
            pc = ax.scatter(x, np.full(5, i), c=f'C{i}', marker='x', s=100,
                            linewidths=i + 1)
            assert pc.get_linewidths() == i + 1

        pc = ax.scatter(x, np.full(5, 3), c='C3', marker='x', s=100,
                        linewidths=[*range(1, 5), None])
        assert_array_equal(pc.get_linewidths(),
                           [*range(1, 5), mpl.rcParams['lines.linewidth']])
