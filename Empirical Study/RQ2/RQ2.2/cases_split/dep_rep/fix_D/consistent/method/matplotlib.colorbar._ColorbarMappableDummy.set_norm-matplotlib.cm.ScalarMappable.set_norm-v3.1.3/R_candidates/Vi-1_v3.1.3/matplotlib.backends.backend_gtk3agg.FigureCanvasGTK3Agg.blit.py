    def blit(self, bbox=None):
        # If bbox is None, blit the entire canvas to gtk. Otherwise
        # blit only the area defined by the bbox.
        if bbox is None:
            bbox = self.figure.bbox

        allocation = self.get_allocation()
        w, h = allocation.width, allocation.height
        x = int(bbox.x0)
        y = h - int(bbox.y1)
        width = int(bbox.x1) - int(bbox.x0)
        height = int(bbox.y1) - int(bbox.y0)

        self._bbox_queue.append(bbox)
        self.queue_draw_area(x, y, width, height)
