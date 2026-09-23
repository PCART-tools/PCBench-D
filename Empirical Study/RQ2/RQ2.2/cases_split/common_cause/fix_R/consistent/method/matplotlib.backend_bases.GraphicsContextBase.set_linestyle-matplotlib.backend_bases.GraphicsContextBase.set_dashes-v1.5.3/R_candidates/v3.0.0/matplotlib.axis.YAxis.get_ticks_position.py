    def get_ticks_position(self):
        """
        Return the ticks position (left, right, both or unknown)
        """
        majt = self.majorTicks[0]
        mT = self.minorTicks[0]

        majorRight = ((not majt.tick1On) and majt.tick2On and
                      (not majt.label1On) and majt.label2On)
        minorRight = ((not mT.tick1On) and mT.tick2On and
                      (not mT.label1On) and mT.label2On)
        if majorRight and minorRight:
            return 'right'

        majorLeft = (majt.tick1On and (not majt.tick2On) and
                     majt.label1On and (not majt.label2On))
        minorLeft = (mT.tick1On and (not mT.tick2On) and
                     mT.label1On and (not mT.label2On))
        if majorLeft and minorLeft:
            return 'left'

        majorDefault = (majt.tick1On and majt.tick2On and
                        majt.label1On and (not majt.label2On))
        minorDefault = (mT.tick1On and mT.tick2On and
                        mT.label1On and (not mT.label2On))
        if majorDefault and minorDefault:
            return 'default'

        return 'unknown'
