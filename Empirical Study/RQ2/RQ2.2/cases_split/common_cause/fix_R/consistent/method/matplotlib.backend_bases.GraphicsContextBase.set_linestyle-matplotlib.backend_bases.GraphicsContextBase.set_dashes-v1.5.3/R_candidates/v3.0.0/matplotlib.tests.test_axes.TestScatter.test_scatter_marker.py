    @image_comparison(baseline_images=['scatter_marker'], remove_text=True,
                      extensions=['png'])
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
