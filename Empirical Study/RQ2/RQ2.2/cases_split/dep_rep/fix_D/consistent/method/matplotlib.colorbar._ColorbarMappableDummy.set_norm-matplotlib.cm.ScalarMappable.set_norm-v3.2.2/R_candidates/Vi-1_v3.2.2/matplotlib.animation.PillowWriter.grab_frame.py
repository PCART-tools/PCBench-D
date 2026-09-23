    def grab_frame(self, **savefig_kwargs):
        from PIL import Image
        buf = BytesIO()
        self._fig.savefig(buf, **dict(savefig_kwargs, format="rgba"))
        renderer = self._fig.canvas.get_renderer()
        self._frames.append(Image.frombuffer(
            "RGBA",
            (int(renderer.width), int(renderer.height)), buf.getbuffer(),
            "raw", "RGBA", 0, 1))
