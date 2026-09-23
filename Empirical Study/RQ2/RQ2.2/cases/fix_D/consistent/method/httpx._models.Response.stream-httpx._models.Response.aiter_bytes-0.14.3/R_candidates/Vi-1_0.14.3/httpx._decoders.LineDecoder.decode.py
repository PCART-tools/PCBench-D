    def decode(self, text: str) -> typing.List[str]:
        lines = []

        if text and self.buffer and self.buffer[-1] == "\r":
            if text.startswith("\n"):
                # Handle the case where we have an "\r\n" split across
                # our previous input, and our new chunk.
                lines.append(self.buffer[:-1] + "\n")
                self.buffer = ""
                text = text[1:]
            else:
                # Handle the case where we have "\r" at the end of our
                # previous input.
                lines.append(self.buffer[:-1] + "\n")
                self.buffer = ""

        while text:
            num_chars = len(text)
            for idx in range(num_chars):
                char = text[idx]
                next_char = None if idx + 1 == num_chars else text[idx + 1]
                if char == "\n":
                    lines.append(self.buffer + text[: idx + 1])
                    self.buffer = ""
                    text = text[idx + 1 :]
                    break
                elif char == "\r" and next_char == "\n":
                    lines.append(self.buffer + text[:idx] + "\n")
                    self.buffer = ""
                    text = text[idx + 2 :]
                    break
                elif char == "\r" and next_char is not None:
                    lines.append(self.buffer + text[:idx] + "\n")
                    self.buffer = ""
                    text = text[idx + 1 :]
                    break
                elif next_char is None:
                    self.buffer += text
                    text = ""
                    break

        return lines
