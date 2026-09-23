    def get_rotation(self):
        angle = text.Text.get_rotation(self)
        trans = self.get_transform()
        x, y = self.get_position()
        new_angles = trans.transform_angles(np.array([angle]),
                                            np.array([[x, y]]))
        return new_angles[0]
