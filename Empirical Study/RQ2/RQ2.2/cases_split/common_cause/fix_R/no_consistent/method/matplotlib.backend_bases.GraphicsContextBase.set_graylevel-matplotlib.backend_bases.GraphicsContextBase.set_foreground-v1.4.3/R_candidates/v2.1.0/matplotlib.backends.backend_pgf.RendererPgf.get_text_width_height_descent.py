    def get_text_width_height_descent(self, s, prop, ismath):
        # check if the math is supposed to be displaystyled
        s = common_texification(s)

        # get text metrics in units of latex pt, convert to display units
        w, h, d = self.latexManager.get_width_height_descent(s, prop)
        # TODO: this should be latex_pt_to_in instead of mpl_pt_to_in
        # but having a little bit more space around the text looks better,
        # plus the bounding box reported by LaTeX is VERY narrow
        f = mpl_pt_to_in * self.dpi
        return w * f, h * f, d * f
