    def set_label_props(self, label, text, color):
        "set the label properties - color, fontsize, text"
        label.set_text(text)
        label.set_color(color)
        label.set_fontproperties(self.labelFontProps)
        label.set_clip_box(self.ax.bbox)
