    def grab_frame(self, **savefig_kwargs):
        from PIL import Image
        buf = BytesIO()
        self.fig.savefig(
            buf, **{**savefig_kwargs, "format": "rgba", "dpi": self.dpi})
        renderer = self.fig.canvas.get_renderer()
        self._frames.append(Image.frombuffer(
            "RGBA", self.frame_size, buf.getbuffer(), "raw", "RGBA", 0, 1))
