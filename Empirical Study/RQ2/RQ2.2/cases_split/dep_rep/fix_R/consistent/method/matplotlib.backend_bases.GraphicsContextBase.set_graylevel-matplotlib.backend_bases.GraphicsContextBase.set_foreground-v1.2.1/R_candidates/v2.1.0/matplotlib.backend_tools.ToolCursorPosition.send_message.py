    def send_message(self, event):
        """Call `matplotlib.backend_managers.ToolManager.message_event`"""
        if self.toolmanager.messagelock.locked():
            return

        message = ' '

        if event.inaxes and event.inaxes.get_navigate():
            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                artists = [a for a in event.inaxes.mouseover_set
                           if a.contains(event) and a.get_visible()]

                if artists:
                    a = max(artists, key=lambda x: x.zorder)
                    if a is not event.inaxes.patch:
                        data = a.get_cursor_data(event)
                        if data is not None:
                            s += ' [%s]' % a.format_cursor_data(data)

                message = s
        self.toolmanager.message_event(message, self)
