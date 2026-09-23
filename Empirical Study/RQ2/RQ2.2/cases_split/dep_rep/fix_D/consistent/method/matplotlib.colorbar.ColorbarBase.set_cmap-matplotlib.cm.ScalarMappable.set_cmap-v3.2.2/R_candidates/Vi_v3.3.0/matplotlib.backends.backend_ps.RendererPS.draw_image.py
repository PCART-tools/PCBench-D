    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]
        imagecmd = "false 3 colorimage"
        data = im[::-1, :, :3]  # Vertically flipped rgb values.
        # data.tobytes().hex() has no spaces, so can be linewrapped by simply
        # splitting data every nchars. It's equivalent to textwrap.fill only
        # much faster.
        nchars = 128
        data = data.tobytes().hex()
        hexlines = "\n".join(
            [
                data[n * nchars:(n + 1) * nchars]
                for n in range(math.ceil(len(data) / nchars))
            ]
        )

        if transform is None:
            matrix = "1 0 0 1 0 0"
            xscale = w / self.image_magnification
            yscale = h / self.image_magnification
        else:
            matrix = " ".join(map(str, transform.frozen().to_values()))
            xscale = 1.0
            yscale = 1.0

        bbox = gc.get_clip_rectangle()
        clippath, clippath_trans = gc.get_clip_path()

        clip = []
        if bbox is not None:
            clip.append('%s clipbox' % _nums_to_str(*bbox.size, *bbox.p0))
        if clippath is not None:
            id = self._get_clip_path(clippath, clippath_trans)
            clip.append('%s' % id)
        clip = '\n'.join(clip)

        self._pswriter.write(f"""\
gsave
{clip}
{x:f} {y:f} translate
[{matrix}] concat
{xscale:f} {yscale:f} scale
/DataString {w:d} string def
{w:d} {h:d} 8 [ {w:d} 0 0 -{h:d} 0 {h:d} ]
{{
currentfile DataString readhexstring pop
}} bind {imagecmd}
{hexlines}
grestore
""")
