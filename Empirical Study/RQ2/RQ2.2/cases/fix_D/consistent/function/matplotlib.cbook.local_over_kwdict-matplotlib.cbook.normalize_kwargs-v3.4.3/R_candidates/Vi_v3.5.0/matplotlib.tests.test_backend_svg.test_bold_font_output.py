@image_comparison(['bold_font_output.svg'])
def test_bold_font_output():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10))
    ax.set_xlabel('nonbold-xlabel')
    ax.set_ylabel('bold-ylabel', fontweight='bold')
    ax.set_title('bold-title', fontweight='bold')
