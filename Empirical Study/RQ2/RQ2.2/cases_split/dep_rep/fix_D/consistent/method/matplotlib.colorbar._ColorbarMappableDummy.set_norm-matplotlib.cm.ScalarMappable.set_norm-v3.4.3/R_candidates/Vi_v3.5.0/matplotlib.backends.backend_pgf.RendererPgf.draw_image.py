    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]
        if w == 0 or h == 0:
            return

        if not os.path.exists(getattr(self.fh, "name", "")):
            raise ValueError(
                "streamed pgf-code does not support raster graphics, consider "
                "using the pgf-to-pdf option")

        # save the images to png files
        path = pathlib.Path(self.fh.name)
        fname_img = "%s-img%d.png" % (path.stem, self.image_counter)
        Image.fromarray(im[::-1]).save(path.parent / fname_img)
        self.image_counter += 1

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
                r"{%s[interpolate=%s,width=%fin,height=%fin]{%s}}" %
                (_get_image_inclusion_command(),
                 interp, w, h, fname_img))
        writeln(self.fh, r"\end{pgfscope}")
