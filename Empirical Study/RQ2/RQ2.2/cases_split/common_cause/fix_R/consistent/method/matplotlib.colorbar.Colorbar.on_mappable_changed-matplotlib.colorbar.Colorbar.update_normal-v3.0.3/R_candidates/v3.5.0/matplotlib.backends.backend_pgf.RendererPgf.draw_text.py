    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        # prepare string for tex
        s = _escape_and_apply_props(s, prop)

        writeln(self.fh, r"\begin{pgfscope}")

        alpha = gc.get_alpha()
        if alpha != 1.0:
            writeln(self.fh, r"\pgfsetfillopacity{%f}" % alpha)
            writeln(self.fh, r"\pgfsetstrokeopacity{%f}" % alpha)
        rgb = tuple(gc.get_rgb())[:3]
        writeln(self.fh, r"\definecolor{textcolor}{rgb}{%f,%f,%f}" % rgb)
        writeln(self.fh, r"\pgfsetstrokecolor{textcolor}")
        writeln(self.fh, r"\pgfsetfillcolor{textcolor}")
        s = r"\color{textcolor}" + s

        dpi = self.figure.dpi
        text_args = []
        if mtext and (
                (angle == 0 or
                 mtext.get_rotation_mode() == "anchor") and
                mtext.get_verticalalignment() != "center_baseline"):
            # if text anchoring can be supported, get the original coordinates
            # and add alignment information
            pos = mtext.get_unitless_position()
            x, y = mtext.get_transform().transform(pos)
            halign = {"left": "left", "right": "right", "center": ""}
            valign = {"top": "top", "bottom": "bottom",
                      "baseline": "base", "center": ""}
            text_args.extend([
                f"x={x/dpi:f}in",
                f"y={y/dpi:f}in",
                halign[mtext.get_horizontalalignment()],
                valign[mtext.get_verticalalignment()],
            ])
        else:
            # if not, use the text layout provided by Matplotlib.
            text_args.append(f"x={x/dpi:f}in, y={y/dpi:f}in, left, base")

        if angle != 0:
            text_args.append("rotate=%f" % angle)

        writeln(self.fh, r"\pgftext[%s]{%s}" % (",".join(text_args), s))
        writeln(self.fh, r"\end{pgfscope}")
