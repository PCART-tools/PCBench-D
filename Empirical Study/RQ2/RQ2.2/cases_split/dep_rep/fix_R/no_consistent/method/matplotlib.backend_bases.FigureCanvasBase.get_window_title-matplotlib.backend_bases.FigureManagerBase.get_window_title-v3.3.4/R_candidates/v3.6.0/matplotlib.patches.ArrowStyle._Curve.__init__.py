        def __init__(self, head_length=.4, head_width=.2, widthA=1., widthB=1.,
                     lengthA=0.2, lengthB=0.2, angleA=0, angleB=0, scaleA=None,
                     scaleB=None):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head, relative to *mutation_scale*.
            head_width : float, default: 0.2
                Width of the arrow head, relative to *mutation_scale*.
            widthA : float, default: 1.0
                Width of the bracket at the beginning of the arrow
            widthB : float, default: 1.0
                Width of the bracket at the end of the arrow
            lengthA : float, default: 0.2
                Length of the bracket at the beginning of the arrow
            lengthB : float, default: 0.2
                Length of the bracket at the end of the arrow
            angleA : float, default 0
                Orientation of the bracket at the beginning, as a
                counterclockwise angle. 0 degrees means perpendicular
                to the line.
            angleB : float, default 0
                Orientation of the bracket at the beginning, as a
                counterclockwise angle. 0 degrees means perpendicular
                to the line.
            scaleA : float, default *mutation_size*
                The mutation_size for the beginning bracket
            scaleB : float, default *mutation_size*
                The mutation_size for the end bracket
            """

            self.head_length, self.head_width = head_length, head_width
            self.widthA, self.widthB = widthA, widthB
            self.lengthA, self.lengthB = lengthA, lengthB
            self.angleA, self.angleB = angleA, angleB
            self.scaleA, self.scaleB = scaleA, scaleB

            self._beginarrow_head = False
            self._beginarrow_bracket = False
            self._endarrow_head = False
            self._endarrow_bracket = False

            if "-" not in self.arrow:
                raise ValueError("arrow must have the '-' between "
                                 "the two heads")

            beginarrow, endarrow = self.arrow.split("-", 1)

            if beginarrow == "<":
                self._beginarrow_head = True
                self._beginarrow_bracket = False
            elif beginarrow == "<|":
                self._beginarrow_head = True
                self._beginarrow_bracket = False
                self.fillbegin = True
            elif beginarrow in ("]", "|"):
                self._beginarrow_head = False
                self._beginarrow_bracket = True
            elif self.beginarrow is True:
                self._beginarrow_head = True
                self._beginarrow_bracket = False

                _api.warn_deprecated('3.5', name="beginarrow",
                                     alternative="arrow")
            elif self.beginarrow is False:
                self._beginarrow_head = False
                self._beginarrow_bracket = False

                _api.warn_deprecated('3.5', name="beginarrow",
                                     alternative="arrow")

            if endarrow == ">":
                self._endarrow_head = True
                self._endarrow_bracket = False
            elif endarrow == "|>":
                self._endarrow_head = True
                self._endarrow_bracket = False
                self.fillend = True
            elif endarrow in ("[", "|"):
                self._endarrow_head = False
                self._endarrow_bracket = True
            elif self.endarrow is True:
                self._endarrow_head = True
                self._endarrow_bracket = False

                _api.warn_deprecated('3.5', name="endarrow",
                                     alternative="arrow")
            elif self.endarrow is False:
                self._endarrow_head = False
                self._endarrow_bracket = False

                _api.warn_deprecated('3.5', name="endarrow",
                                     alternative="arrow")

            super().__init__()
