    def set_message(self, message):
        _macosx.NavigationToolbar2.set_message(self, message.encode('utf-8'))
