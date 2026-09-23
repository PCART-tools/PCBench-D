@image_comparison(['line_dashes'], remove_text=True)
def test_line_dashes():
    fig, ax = plt.subplots()

    ax.plot(range(10), linestyle=(0, (3, 3)), lw=5)
