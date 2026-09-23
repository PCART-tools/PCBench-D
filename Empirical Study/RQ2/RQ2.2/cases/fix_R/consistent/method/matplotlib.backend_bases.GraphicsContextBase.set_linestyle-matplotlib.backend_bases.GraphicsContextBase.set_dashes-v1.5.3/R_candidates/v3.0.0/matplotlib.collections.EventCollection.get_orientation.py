    def get_orientation(self):
        '''
        get the orientation of the event line, may be:
        [ 'horizontal' | 'vertical' ]
        '''
        return 'horizontal' if self.is_horizontal() else 'vertical'
