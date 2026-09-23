        def __init__(self, armA=0., armB=0., fraction=0.3, angle=None):
            """
            Parameters
            ----------
            armA : float
                minimum length of armA

            armB : float
                minimum length of armB

            fraction : float
                a fraction of the distance between two points that
                will be added to armA and armB.

            angle : float or None
                angle of the connecting line (if None, parallel
                to A and B)
            """
            self.armA = armA
            self.armB = armB
            self.fraction = fraction
            self.angle = angle
