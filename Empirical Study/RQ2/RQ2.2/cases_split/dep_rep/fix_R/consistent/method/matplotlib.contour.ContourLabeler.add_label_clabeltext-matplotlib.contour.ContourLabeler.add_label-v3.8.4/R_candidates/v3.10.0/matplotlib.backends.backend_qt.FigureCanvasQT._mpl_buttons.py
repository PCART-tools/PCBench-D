    @staticmethod
    def _mpl_buttons(buttons):
        buttons = _to_int(buttons)
        # State *after* press/release.
        return {button for mask, button in FigureCanvasQT.buttond.items()
                if _to_int(mask) & buttons}
