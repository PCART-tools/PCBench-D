    def write_comment(self, s):
        self.f.write(f"% {s}\n".encode())
