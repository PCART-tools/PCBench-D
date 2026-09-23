    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]
        if w == 0 or h == 0:
            return

        # save the images to png files
        path = os.path.dirname(self.fh.name)
        fname = os.path.splitext(os.path.basename(self.fh.name))[0]
        fname_img = "%s-img%d.png" % (fname, self.image_counter)
        self.image_counter += 1
        _png.write_png(im[::-1], os.path.join(path, fname_img))

        # reference the image in the pgf picture
        writeln(self.fh, r"\begin{pgfscope}")
        self._print_pgf_clip(gc)
        f = 1. / self.dpi  # from display coords to inch
        if transform is None:
            writeln(self.fh,
                    r"\pgfsys@transformshift{%fin}{%fin}" % (x * f, y * f))
            w, h = w * f, h * f
        else:
            tr1, tr2, tr3, tr4, tr5, tr6 = transform.frozen().to_values()
            writeln(self.fh,
                    r"\pgfsys@transformcm{%f}{%f}{%f}{%f}{%fin}{%fin}" %
                    (tr1 * f, tr2 * f, tr3 * f, tr4 * f,
                     (tr5 + x) * f, (tr6 + y) * f))
            w = h = 1  # scale is already included in the transform
        interp = str(transform is None).lower()  # interpolation in PDF reader
        writeln(self.fh,
                r"\pgftext[left,bottom]"
                r"{\pgfimage[interpolate=%s,width=%fin,height=%fin]{%s}}" %
                (interp, w, h, fname_img))
        writeln(self.fh, r"\end{pgfscope}")
