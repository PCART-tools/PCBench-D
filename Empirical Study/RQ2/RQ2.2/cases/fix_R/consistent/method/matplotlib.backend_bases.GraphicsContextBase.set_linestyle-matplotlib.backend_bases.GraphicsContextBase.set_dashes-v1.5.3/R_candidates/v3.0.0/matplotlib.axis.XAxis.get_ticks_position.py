    def get_ticks_position(self):
        """
        Return the ticks position (top, bottom, default or unknown)
        """
        majt = self.majorTicks[0]
        mT = self.minorTicks[0]

        majorTop = ((not majt.tick1On) and majt.tick2On and
                    (not majt.label1On) and majt.label2On)
        minorTop = ((not mT.tick1On) and mT.tick2On and
                    (not mT.label1On) and mT.label2On)
        if majorTop and minorTop:
            return 'top'

        MajorBottom = (majt.tick1On and (not majt.tick2On) and
                       majt.label1On and (not majt.label2On))
        MinorBottom = (mT.tick1On and (not mT.tick2On) and
                       mT.label1On and (not mT.label2On))
        if MajorBottom and MinorBottom:
            return 'bottom'

        majorDefault = (majt.tick1On and majt.tick2On and
                        majt.label1On and (not majt.label2On))
        minorDefault = (mT.tick1On and mT.tick2On and
                        mT.label1On and (not mT.label2On))
        if majorDefault and minorDefault:
            return 'default'

        return 'unknown'
