    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]
        imagecmd = "false 3 colorimage"
        data = im[::-1, :, :3]  # Vertically flipped rgb values.
        # data.tobytes().hex() has no spaces, so can be linewrapped by relying
        # on textwrap.fill breaking long words.
        hexlines = textwrap.fill(data.tobytes().hex(), 128)

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
            clipx, clipy, clipw, cliph = bbox.bounds
            clip.append(
                '%s clipbox' % _nums_to_str(clipw, cliph, clipx, clipy))
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
