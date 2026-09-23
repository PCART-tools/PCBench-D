    def reverse(self, i):
        orig = ffi.new("int *", i)
        chars = ffi.cast("unsigned char *", orig)
        chars[0], chars[1], chars[2], chars[3] = chars[3], chars[2], chars[1], chars[0]
        return ffi.cast("int *", chars)[0]
