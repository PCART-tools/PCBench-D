    def run(self):
        latex = ''.join(self.content)
        node = latex_math(self.block_text)
        node['latex'] = latex
        node['fontset'] = self.options.get('fontset', 'cm')
        return [node]
