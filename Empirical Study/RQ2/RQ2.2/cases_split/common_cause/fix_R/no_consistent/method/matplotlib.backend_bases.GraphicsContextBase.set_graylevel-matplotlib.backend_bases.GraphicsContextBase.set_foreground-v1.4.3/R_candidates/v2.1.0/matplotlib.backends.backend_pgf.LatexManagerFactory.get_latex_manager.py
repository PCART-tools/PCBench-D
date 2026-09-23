    @staticmethod
    def get_latex_manager():
        texcommand = get_texcommand()
        latex_header = LatexManager._build_latex_header()
        prev = LatexManagerFactory.previous_instance

        # Check if the previous instance of LatexManager can be reused.
        if (prev and prev.latex_header == latex_header
                and prev.texcommand == texcommand):
            if rcParams["pgf.debug"]:
                print("reusing LatexManager")
            return prev
        else:
            if rcParams["pgf.debug"]:
                print("creating LatexManager")
            new_inst = LatexManager()
            LatexManagerFactory.previous_instance = new_inst
            return new_inst
