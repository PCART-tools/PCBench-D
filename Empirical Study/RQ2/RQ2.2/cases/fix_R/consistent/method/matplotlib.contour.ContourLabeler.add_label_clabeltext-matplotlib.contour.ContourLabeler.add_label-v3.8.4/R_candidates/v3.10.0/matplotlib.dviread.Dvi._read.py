    def _read(self):
        """
        Read one page from the file. Return True if successful,
        False if there were no more pages.
        """
        # Pages appear to start with the sequence
        #   bop (begin of page)
        #   xxx comment
        #   <push, ..., pop>  # if using chemformula
        #   down
        #   push
        #     down
        #     <push, push, xxx, right, xxx, pop, pop>  # if using xcolor
        #     down
        #     push
        #       down (possibly multiple)
        #       push  <=  here, v is the baseline position.
        #         etc.
        # (dviasm is useful to explore this structure.)
        # Thus, we use the vertical position at the first time the stack depth
        # reaches 3, while at least three "downs" have been executed (excluding
        # those popped out (corresponding to the chemformula preamble)), as the
        # baseline (the "down" count is necessary to handle xcolor).
        down_stack = [0]
        self._baseline_v = None
        while True:
            byte = self.file.read(1)[0]
            self._dtable[byte](self, byte)
            if self._missing_font:
                raise self._missing_font.to_exception()
            name = self._dtable[byte].__name__
            if name == "_push":
                down_stack.append(down_stack[-1])
            elif name == "_pop":
                down_stack.pop()
            elif name == "_down":
                down_stack[-1] += 1
            if (self._baseline_v is None
                    and len(getattr(self, "stack", [])) == 3
                    and down_stack[-1] >= 4):
                self._baseline_v = self.v
            if byte == 140:                         # end of page
                return True
            if self.state is _dvistate.post_post:   # end of file
                self.close()
                return False
