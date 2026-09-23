    def set_orientation(self, orientation=None):
        '''
        set the orientation of the event line
        [ 'horizontal' | 'vertical' | None ]
        defaults to 'horizontal' if not specified or None
        '''
        if (orientation is None or orientation.lower() == 'none' or
                orientation.lower() == 'horizontal'):
            is_horizontal = True
        elif orientation.lower() == 'vertical':
            is_horizontal = False
        else:
            cbook._check_in_list(['horizontal', 'vertical'],
                                 orientation=orientation)
        if is_horizontal == self.is_horizontal():
            return
        self.switch_orientation()
