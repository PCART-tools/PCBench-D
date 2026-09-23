    def grab_frame(self, **savefig_kwargs):
        from PIL import Image
        buf = BytesIO()
        self._fig.savefig(buf, **dict(savefig_kwargs, format="rgba"))
        renderer = self._fig.canvas.get_renderer()
        # Using frombuffer / getbuffer may be slightly more efficient, but
        # Py3-only.
        self._frames.append(Image.frombytes(
            "RGBA",
            (int(renderer.width), int(renderer.height)),
            buf.getvalue()))
