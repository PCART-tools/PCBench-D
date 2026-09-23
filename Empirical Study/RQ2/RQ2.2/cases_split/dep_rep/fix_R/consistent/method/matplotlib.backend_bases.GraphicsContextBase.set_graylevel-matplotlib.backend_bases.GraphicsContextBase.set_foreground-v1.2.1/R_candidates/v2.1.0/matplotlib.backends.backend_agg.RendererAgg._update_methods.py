    def _update_methods(self):
        self.draw_quad_mesh = self._renderer.draw_quad_mesh
        self.draw_gouraud_triangle = self._renderer.draw_gouraud_triangle
        self.draw_gouraud_triangles = self._renderer.draw_gouraud_triangles
        self.draw_image = self._renderer.draw_image
        self.copy_from_bbox = self._renderer.copy_from_bbox
        self.get_content_extents = self._renderer.get_content_extents
