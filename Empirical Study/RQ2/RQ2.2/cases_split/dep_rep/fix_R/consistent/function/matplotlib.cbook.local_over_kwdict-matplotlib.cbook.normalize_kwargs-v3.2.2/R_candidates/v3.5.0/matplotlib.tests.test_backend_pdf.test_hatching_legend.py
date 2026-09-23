@image_comparison(['hatching_legend.pdf'])
def test_hatching_legend():
    """Test for correct hatching on patches in legend"""
    fig = plt.figure(figsize=(1, 2))

    a = plt.Rectangle([0, 0], 0, 0, facecolor="green", hatch="XXXX")
    b = plt.Rectangle([0, 0], 0, 0, facecolor="blue", hatch="XXXX")

    fig.legend([a, b, a, b], ["", "", "", ""])
