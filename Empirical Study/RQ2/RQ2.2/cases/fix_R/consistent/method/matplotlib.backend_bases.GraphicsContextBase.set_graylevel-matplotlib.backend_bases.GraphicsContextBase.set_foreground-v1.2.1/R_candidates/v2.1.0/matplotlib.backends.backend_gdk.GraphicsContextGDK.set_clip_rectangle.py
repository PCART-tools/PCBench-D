    def set_clip_rectangle(self, rectangle):
        GraphicsContextBase.set_clip_rectangle(self, rectangle)
        if rectangle is None:
            return
        l,b,w,h = rectangle.bounds
        rectangle = (int(l), self.renderer.height-int(b+h)+1,
                     int(w), int(h))
        #rectangle = (int(l), self.renderer.height-int(b+h),
        #             int(w+1), int(h+2))
        self.gdkGC.set_clip_rectangle(rectangle)
