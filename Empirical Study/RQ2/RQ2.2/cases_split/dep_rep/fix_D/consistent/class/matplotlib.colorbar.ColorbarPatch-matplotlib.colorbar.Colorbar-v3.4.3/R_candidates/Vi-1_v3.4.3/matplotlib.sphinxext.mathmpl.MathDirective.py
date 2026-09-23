class MathDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'fontset': fontset_choice}

    def run(self):
        latex = ''.join(self.content)
        node = latex_math(self.block_text)
        node['latex'] = latex
        node['fontset'] = self.options.get('fontset', 'cm')
        return [node]
