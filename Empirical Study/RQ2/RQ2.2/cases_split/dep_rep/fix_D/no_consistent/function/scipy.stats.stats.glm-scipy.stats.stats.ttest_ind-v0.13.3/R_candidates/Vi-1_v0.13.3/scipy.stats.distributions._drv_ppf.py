def _drv_ppf(self, q, *args):
    indx = argmax((self.qvals >= q),axis=-1)
    return self.Finv[self.qvals[indx]]
