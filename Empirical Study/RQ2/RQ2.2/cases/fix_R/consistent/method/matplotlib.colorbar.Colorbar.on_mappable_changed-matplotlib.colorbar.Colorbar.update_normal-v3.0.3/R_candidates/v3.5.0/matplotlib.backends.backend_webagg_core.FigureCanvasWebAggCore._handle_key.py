    def _handle_key(self, event):
        key = _handle_key(event['key'])
        e_type = event['type']
        guiEvent = event.get('guiEvent', None)
        if e_type == 'key_press':
            self.key_press_event(key, guiEvent=guiEvent)
        elif e_type == 'key_release':
            self.key_release_event(key, guiEvent=guiEvent)
