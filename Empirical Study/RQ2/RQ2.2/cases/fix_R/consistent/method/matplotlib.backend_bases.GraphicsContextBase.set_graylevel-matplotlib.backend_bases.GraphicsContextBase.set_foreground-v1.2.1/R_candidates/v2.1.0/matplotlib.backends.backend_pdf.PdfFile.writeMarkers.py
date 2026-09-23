    def writeMarkers(self):
        for ((pathops, fill, stroke, joinstyle, capstyle),
             (name, ob, bbox, lw)) in six.iteritems(self.markers):
            bbox = bbox.padded(lw * 0.5)
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
