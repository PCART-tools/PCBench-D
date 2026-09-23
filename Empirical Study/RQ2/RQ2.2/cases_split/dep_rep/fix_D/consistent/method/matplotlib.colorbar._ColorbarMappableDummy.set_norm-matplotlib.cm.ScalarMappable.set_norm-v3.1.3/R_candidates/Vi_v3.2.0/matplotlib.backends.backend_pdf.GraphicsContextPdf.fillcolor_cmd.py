    def fillcolor_cmd(self, rgb):
        if rgb is None or rcParams['pdf.inheritcolor']:
            return []
        elif rgb[0] == rgb[1] == rgb[2]:
            return [rgb[0], Op.setgray_nonstroke]
        else:
            return [*rgb[:3], Op.setrgb_nonstroke]
