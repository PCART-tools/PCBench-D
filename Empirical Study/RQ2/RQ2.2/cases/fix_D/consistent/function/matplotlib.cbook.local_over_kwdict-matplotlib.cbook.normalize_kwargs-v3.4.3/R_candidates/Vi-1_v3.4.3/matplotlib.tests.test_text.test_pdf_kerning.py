@image_comparison(['text_pdf_kerning.pdf'], style='mpl20')
def test_pdf_kerning():
    plt.figure()
    plt.figtext(0.1, 0.5, "ATATATATATATATATATA", size=30)
