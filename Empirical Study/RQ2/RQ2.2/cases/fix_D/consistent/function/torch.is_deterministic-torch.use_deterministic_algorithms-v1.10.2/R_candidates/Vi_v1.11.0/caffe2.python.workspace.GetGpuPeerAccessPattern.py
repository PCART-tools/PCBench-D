    def GetGpuPeerAccessPattern():
        return np.asarray(C.get_hip_peer_access_pattern())
