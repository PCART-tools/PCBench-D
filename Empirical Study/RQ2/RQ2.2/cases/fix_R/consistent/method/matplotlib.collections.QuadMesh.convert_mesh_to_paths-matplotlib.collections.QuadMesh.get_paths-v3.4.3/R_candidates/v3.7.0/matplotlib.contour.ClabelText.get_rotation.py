    def get_rotation(self):
        new_angle, = self.get_transform().transform_angles(
            [super().get_rotation()], [self.get_position()])
        return new_angle
