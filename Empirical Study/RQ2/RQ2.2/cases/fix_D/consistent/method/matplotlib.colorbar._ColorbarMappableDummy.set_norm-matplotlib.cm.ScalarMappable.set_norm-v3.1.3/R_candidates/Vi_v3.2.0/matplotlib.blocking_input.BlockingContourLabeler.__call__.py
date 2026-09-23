    def __call__(self, inline, inline_spacing=5, n=-1, timeout=-1):
        self.inline = inline
        self.inline_spacing = inline_spacing
        BlockingMouseInput.__call__(self, n=n, timeout=timeout,
                                    show_clicks=False)
