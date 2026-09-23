    def _read(self):
        """
        Read one page from the file. Return True if successful,
        False if there were no more pages.
        """
        packet_char, packet_ends = None, None
        packet_len, packet_width = None, None
        while True:
            byte = self.file.read(1)[0]
            # If we are in a packet, execute the dvi instructions
            if self.state is _dvistate.inpage:
                byte_at = self.file.tell()-1
                if byte_at == packet_ends:
                    self._finalize_packet(packet_char, packet_width)
                    packet_len, packet_char, packet_width = None, None, None
                    # fall through to out-of-packet code
                elif byte_at > packet_ends:
                    raise ValueError("Packet length mismatch in vf file")
                else:
                    if byte in (139, 140) or byte >= 243:
                        raise ValueError(
                            "Inappropriate opcode %d in vf file" % byte)
                    Dvi._dtable[byte](self, byte)
                    continue

            # We are outside a packet
            if byte < 242:          # a short packet (length given by byte)
                packet_len = byte
                packet_char, packet_width = self._arg(1), self._arg(3)
                packet_ends = self._init_packet(byte)
                self.state = _dvistate.inpage
            elif byte == 242:       # a long packet
                packet_len, packet_char, packet_width = \
                            [self._arg(x) for x in (4, 4, 4)]
                self._init_packet(packet_len)
            elif 243 <= byte <= 246:
                k = self._arg(byte - 242, byte == 246)
                c, s, d, a, l = [self._arg(x) for x in (4, 4, 4, 1, 1)]
                self._fnt_def_real(k, c, s, d, a, l)
                if self._first_font is None:
                    self._first_font = k
            elif byte == 247:       # preamble
                i, k = self._arg(1), self._arg(1)
                x = self.file.read(k)
                cs, ds = self._arg(4), self._arg(4)
                self._pre(i, x, cs, ds)
            elif byte == 248:       # postamble (just some number of 248s)
                break
            else:
                raise ValueError("unknown vf opcode %d" % byte)
