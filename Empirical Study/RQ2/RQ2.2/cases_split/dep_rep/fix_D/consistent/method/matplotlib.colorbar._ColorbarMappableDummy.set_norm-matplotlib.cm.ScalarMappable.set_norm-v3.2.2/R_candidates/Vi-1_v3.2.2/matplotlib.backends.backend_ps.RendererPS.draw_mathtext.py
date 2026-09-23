    def draw_mathtext(self, gc, x, y, s, prop, angle):
        """Draw the math text using matplotlib.mathtext."""
        if debugPS:
            self._pswriter.write("% mathtext\n")

        width, height, descent, pswriter, used_characters = \
            self.mathtext_parser.parse(s, 72, prop)
        self.merge_used_characters(used_characters)
        self.set_color(*gc.get_rgb())
        thetext = pswriter.getvalue()
        self._pswriter.write(f"""\
gsave
{x:f} {y:f} translate
{angle:f} rotate
{thetext}
grestore
""")
