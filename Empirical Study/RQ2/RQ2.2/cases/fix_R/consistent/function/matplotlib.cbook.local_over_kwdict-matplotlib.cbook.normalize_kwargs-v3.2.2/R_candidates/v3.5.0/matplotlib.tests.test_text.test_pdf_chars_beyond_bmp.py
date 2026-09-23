@image_comparison(['text_pdf_chars_beyond_bmp.pdf'], style='mpl20')
def test_pdf_chars_beyond_bmp():
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['mathtext.fontset'] = 'stixsans'
    plt.figure()
    plt.figtext(0.1, 0.5, "Mass $m$ \U00010308", size=30)
