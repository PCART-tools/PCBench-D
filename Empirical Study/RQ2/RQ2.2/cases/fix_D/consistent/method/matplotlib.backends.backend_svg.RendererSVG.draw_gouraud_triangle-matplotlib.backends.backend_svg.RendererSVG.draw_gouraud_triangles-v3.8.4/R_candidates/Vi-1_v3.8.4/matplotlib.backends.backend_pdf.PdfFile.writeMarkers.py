    def writeMarkers(self):
        for ((pathops, fill, stroke, joinstyle, capstyle),
             (name, ob, bbox, lw)) in self.markers.items():
            # bbox wraps the exact limits of the control points, so half a line
            # will appear outside it. If the join style is miter and the line
            # is not parallel to the edge, then the line will extend even
            # further. From the PDF specification, Section 8.4.3.5, the miter
            # limit is miterLength / lineWidth and from Table 52, the default
            # is 10. With half the miter length outside, that works out to the
            # following padding:
            bbox = bbox.padded(lw * 5)
            self.beginStream(
                ob.id, None,
                {'Type': Name('XObject'), 'Subtype': Name('Form'),
                 'BBox': list(bbox.extents)})
            self.output(GraphicsContextPdf.joinstyles[joinstyle],
                        Op.setlinejoin)
            self.output(GraphicsContextPdf.capstyles[capstyle], Op.setlinecap)
            self.output(*pathops)
            self.output(Op.paint_path(fill, stroke))
            self.endStream()
