    def rgb_cmd(self, rgb):
        if rcParams['pdf.inheritcolor']:
            return []
        if rgb[0] == rgb[1] == rgb[2]:
            return [rgb[0], Op.setgray_stroke]
        else:
            return list(rgb[:3]) + [Op.setrgb_stroke]
