@image_comparison(baseline_images=['contour_closed_line_loop'],
                  extensions=['png'], remove_text=True)
def test_contour_closed_line_loop():
    # github issue 19568.
    z = [[0, 0, 0], [0, 2, 0], [0, 0, 0], [2, 1, 2]]

    fig, ax = plt.subplots(figsize=(2, 2))
    ax.contour(z, [0.5], linewidths=[20], alpha=0.7)
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-0.1, 3.1)
