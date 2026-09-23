    def _put_rule_real(self, a, b):
        if a > 0 and b > 0:
            self.boxes.append(Box(self.h, self.v, a, b))
