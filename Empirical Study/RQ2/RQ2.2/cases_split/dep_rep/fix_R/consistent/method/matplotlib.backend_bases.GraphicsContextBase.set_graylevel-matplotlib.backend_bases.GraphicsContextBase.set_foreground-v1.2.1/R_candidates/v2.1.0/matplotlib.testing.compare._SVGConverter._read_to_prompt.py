    def _read_to_prompt(self):
        """Did Inkscape reach the prompt without crashing?
        """
        stream = iter(functools.partial(self._proc.stdout.read, 1), b"")
        prompt = (b"\n", b">")
        n = len(prompt)
        its = itertools.tee(stream, n)
        for i, it in enumerate(its):
            next(itertools.islice(it, i, i), None)  # Advance `it` by `i`.
        while True:
            window = tuple(map(next, its))
            if len(window) != n:
                # Ran out of data -- one of the `next(it)` raised
                # StopIteration, so the tuple is shorter.
                return False
            if self._proc.poll() is not None:
                # Inkscape exited.
                return False
            if window == prompt:
                # Successfully read until prompt.
                return True
