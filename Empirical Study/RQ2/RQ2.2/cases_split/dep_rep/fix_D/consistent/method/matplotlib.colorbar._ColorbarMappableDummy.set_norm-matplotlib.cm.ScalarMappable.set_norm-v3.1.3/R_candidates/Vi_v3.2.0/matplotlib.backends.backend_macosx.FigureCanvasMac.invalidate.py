    @cbook.deprecated("3.2", alternative="draw_idle()")
    def invalidate(self):
        return self.draw_idle()
