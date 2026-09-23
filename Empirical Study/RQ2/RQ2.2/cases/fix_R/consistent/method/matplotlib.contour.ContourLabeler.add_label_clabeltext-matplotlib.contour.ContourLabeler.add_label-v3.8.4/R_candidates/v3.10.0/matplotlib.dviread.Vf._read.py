    def _read(self):
        """
        Read one page from the file. Return True if successful,
        False if there were no more pages.
        """
        packet_char = packet_ends = None
        packet_len = packet_width = None
        while True:
            byte = self.file.read(1)[0]
            # If we are in a packet, execute the dvi instructions
            if self.state is _dvistate.inpage:
                byte_at = self.file.tell()-1
                if byte_at == packet_ends:
                    self._finalize_packet(packet_char, packet_width)
                    packet_len = packet_char = packet_width = None
                    # fall through to out-of-packet code
                elif byte_at > packet_ends:
                    raise ValueError("Packet length mismatch in vf file")
                else:
                    if byte in (139, 140) or byte >= 243:
                        raise ValueError(f"Inappropriate opcode {byte} in vf file")
                    Dvi._dtable[byte](self, byte)
                    continue

            # We are outside a packet
            if byte < 242:          # a short packet (length given by byte)
                packet_len = byte
                packet_char = self._read_arg(1)
                packet_width = self._read_arg(3)
                packet_ends = self._init_packet(byte)
                self.state = _dvistate.inpage
            elif byte == 242:       # a long packet
                packet_len = self._read_arg(4)
                packet_char = self._read_arg(4)
                packet_width = self._read_arg(4)
                self._init_packet(packet_len)
            elif 243 <= byte <= 246:
                k = self._read_arg(byte - 242, byte == 246)
                c = self._read_arg(4)
                s = self._read_arg(4)
                d = self._read_arg(4)
                a = self._read_arg(1)
                l = self._read_arg(1)
                self._fnt_def_real(k, c, s, d, a, l)
                if self._first_font is None:
                    self._first_font = k
            elif byte == 247:       # preamble
                i = self._read_arg(1)
                k = self._read_arg(1)
                x = self.file.read(k)
                cs = self._read_arg(4)
                ds = self._read_arg(4)
                self._pre(i, x, cs, ds)
            elif byte == 248:       # postamble (just some number of 248s)
                break
            else:
                raise ValueError(f"Unknown vf opcode {byte}")
