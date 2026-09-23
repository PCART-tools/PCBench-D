    def get_rotation(self):
        new_angle, = self.get_transform().transform_angles(
            [text.Text.get_rotation(self)], [self.get_position()])
        return new_angle
