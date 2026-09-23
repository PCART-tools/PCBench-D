    def __contains__(self, o):
        if isinstance(o, Point):
            x = Dummy('x', real=True)
            y = Dummy('y', real=True)

            res = self.equation(x, y).subs({x: o.x, y: o.y})
            return trigsimp(simplify(res)) is S.Zero
        elif isinstance(o, Ellipse):
            return self == o
        return False
