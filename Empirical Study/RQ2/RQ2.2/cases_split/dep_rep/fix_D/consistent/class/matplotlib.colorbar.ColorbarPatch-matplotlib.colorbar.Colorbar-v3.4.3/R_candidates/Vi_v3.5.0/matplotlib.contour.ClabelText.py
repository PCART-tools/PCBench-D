class ClabelText(text.Text):
    """
    Unlike the ordinary text, the get_rotation returns an updated
    angle in the pixel coordinate assuming that the input rotation is
    an angle in data coordinate (or whatever transform set).
    """

    def get_rotation(self):
        new_angle, = self.get_transform().transform_angles(
            [super().get_rotation()], [self.get_position()])
        return new_angle
