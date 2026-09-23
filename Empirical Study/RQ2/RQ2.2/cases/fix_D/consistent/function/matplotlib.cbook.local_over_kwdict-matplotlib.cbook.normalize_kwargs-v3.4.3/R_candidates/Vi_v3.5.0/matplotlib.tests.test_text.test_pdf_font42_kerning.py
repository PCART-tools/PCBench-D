@image_comparison(['text_pdf_font42_kerning.pdf'], style='mpl20')
def test_pdf_font42_kerning():
    plt.rcParams['pdf.fonttype'] = 42
    plt.figure()
    plt.figtext(0.1, 0.5, "ATAVATAVATAVATAVATA", size=30)
