    def draw(self, renderer):
        # docstring inherited
        conn_same_style = []

        # Figure out which connectors have the same style as the box, so should
        # be drawn as a single path.
        for conn in self.connectors or []:
            if conn.get_visible():
                drawn = False
                for s in _shared_properties:
                    if artist.getp(self._rectangle, s) != artist.getp(conn, s):
                        # Draw this connector by itself
                        conn.draw(renderer)
                        drawn = True
                        break

                if not drawn:
                    # Connector has same style as box.
                    conn_same_style.append(conn)

        if conn_same_style:
            # Since at least one connector has the same style as the rectangle, draw
            # them as a compound path.
            artists = [self._rectangle] + conn_same_style
            paths = [a.get_transform().transform_path(a.get_path()) for a in artists]
            path = Path.make_compound_path(*paths)

            # Create a temporary patch to draw the path.
            p = PathPatch(path)
            p.update_from(self._rectangle)
            p.set_transform(transforms.IdentityTransform())
            p.draw(renderer)

            return

        # Just draw the rectangle
        self._rectangle.draw(renderer)
