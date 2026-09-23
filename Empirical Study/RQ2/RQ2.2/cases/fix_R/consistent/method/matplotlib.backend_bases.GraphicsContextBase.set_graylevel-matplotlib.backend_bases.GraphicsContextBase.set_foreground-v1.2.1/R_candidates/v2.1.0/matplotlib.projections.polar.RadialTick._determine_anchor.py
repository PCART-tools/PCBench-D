    def _determine_anchor(self, angle, start):
        if start:
            if -90 <= angle <= 90:
                return 'left', 'center'
            else:
                return 'right', 'center'
        else:
            if -90 <= angle <= 90:
                return 'right', 'center'
            else:
                return 'left', 'center'
