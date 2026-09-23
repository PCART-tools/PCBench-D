    @cbook.deprecated("2.2")
    def onRemove(self, ev):
        """
        Mouse event processor which removes the top artist
        under the cursor.  Connect this to the 'mouse_press_event'
        using::

            canvas.mpl_connect('mouse_press_event',canvas.onRemove)
        """
        # Find the top artist under the cursor
        under = cbook._topmost_artist(self.figure.hitlist(ev))
        h = None
        if under:
            h = under[-1]

        # Try deleting that artist, or its parent if you
        # can't delete the artist
        while h:
            if h.remove():
                self.draw_idle()
                break
            parent = None
            for p in under:
                if h in p.get_children():
                    parent = p
                    break
            h = parent
