    def _print_png_to_fh(self, fh, *args, **kwargs):
        converter = make_pdf_to_png_converter()

        try:
            # create temporary directory for pdf creation and png conversion
            tmpdir = tempfile.mkdtemp(prefix="mpl_pgf_")
            fname_pdf = os.path.join(tmpdir, "figure.pdf")
            fname_png = os.path.join(tmpdir, "figure.png")
            # create pdf and try to convert it to png
            self.print_pdf(fname_pdf, *args, **kwargs)
            converter(fname_pdf, fname_png, dpi=self.figure.dpi)
            # copy file contents to target
            with open(fname_png, "rb") as fh_src:
                shutil.copyfileobj(fh_src, fh)
        finally:
            try:
                shutil.rmtree(tmpdir)
            except:
                TmpDirCleaner.add(tmpdir)
