    def draw_image(self, gc, x, y, im, transform=None):
        """
        Draw the Image instance into the current axes; x is the
        distance in pixels from the left hand side of the canvas and y
        is the distance from bottom
        """

        h, w, bits, imagecmd = self._get_image_h_w_bits_command(im)
        hexlines = b'\n'.join(self._hex_lines(bits)).decode('ascii')

        if transform is None:
            matrix = "1 0 0 1 0 0"
            xscale = w / self.image_magnification
            yscale = h / self.image_magnification
        else:
            matrix = " ".join(map(str, transform.frozen().to_values()))
            xscale = 1.0
            yscale = 1.0

        figh = self.height * 72

        bbox = gc.get_clip_rectangle()
        clippath, clippath_trans = gc.get_clip_path()

        clip = []
        if bbox is not None:
            clipx,clipy,clipw,cliph = bbox.bounds
            clip.append('%s clipbox' % _nums_to_str(clipw, cliph, clipx, clipy))
        if clippath is not None:
            id = self._get_clip_path(clippath, clippath_trans)
            clip.append('%s' % id)
        clip = '\n'.join(clip)

        ps = """gsave
%(clip)s
%(x)s %(y)s translate
[%(matrix)s] concat
%(xscale)s %(yscale)s scale
/DataString %(w)s string def
%(w)s %(h)s 8 [ %(w)s 0 0 -%(h)s 0 %(h)s ]
{
currentfile DataString readhexstring pop
} bind %(imagecmd)s
%(hexlines)s
grestore
""" % locals()
        self._pswriter.write(ps)
