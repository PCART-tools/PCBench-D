    @staticmethod
    def _mpl_buttons(event):  # See _mpl_modifiers.
        # NOTE: This fails to report multiclicks on macOS; only one button is
        # reported (multiclicks work correctly on Linux & Windows).
        modifiers = [
            # macOS appears to swap right and middle (look for "Swap buttons
            # 2/3" in tk/macosx/tkMacOSXMouseEvent.c).
            (MouseButton.LEFT, 1 << 8),
            (MouseButton.RIGHT, 1 << 9),
            (MouseButton.MIDDLE, 1 << 10),
            (MouseButton.BACK, 1 << 11),
            (MouseButton.FORWARD, 1 << 12),
        ] if sys.platform == "darwin" else [
            (MouseButton.LEFT, 1 << 8),
            (MouseButton.MIDDLE, 1 << 9),
            (MouseButton.RIGHT, 1 << 10),
            (MouseButton.BACK, 1 << 11),
            (MouseButton.FORWARD, 1 << 12),
        ]
        # State *before* press/release.
        return [name for name, mask in modifiers if event.state & mask]
