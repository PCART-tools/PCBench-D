    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # prepare string for tex
        s = common_texification(s)
        prop_cmds = _font_properties_str(prop)
        s = r"%s %s" % (prop_cmds, s)


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

        f = 1.0 / self.figure.dpi
        text_args = []
        if mtext and (
                (angle == 0 or
                 mtext.get_rotation_mode() == "anchor") and
                mtext.get_va() != "center_baseline"):
            # if text anchoring can be supported, get the original coordinates
            # and add alignment information
            pos = mtext.get_unitless_position()
            x, y = mtext.get_transform().transform_point(pos)
            text_args.append("x=%fin" % (x * f))
            text_args.append("y=%fin" % (y * f))

            halign = {"left": "left", "right": "right", "center": ""}
            valign = {"top": "top", "bottom": "bottom",
                      "baseline": "base", "center": ""}
            text_args.append(halign[mtext.get_ha()])
            text_args.append(valign[mtext.get_va()])
        else:
            # if not, use the text layout provided by matplotlib
            text_args.append("x=%fin" % (x * f))
            text_args.append("y=%fin" % (y * f))
            text_args.append("left")
            text_args.append("base")

        if angle != 0:
            text_args.append("rotate=%f" % angle)

        writeln(self.fh, r"\pgftext[%s]{%s}" % (",".join(text_args), s))
        writeln(self.fh, r"\end{pgfscope}")
