def test_pdfpages_fspath():
    with PdfPages(Path(os.devnull)) as pdf:
        pdf.savefig(plt.figure())
