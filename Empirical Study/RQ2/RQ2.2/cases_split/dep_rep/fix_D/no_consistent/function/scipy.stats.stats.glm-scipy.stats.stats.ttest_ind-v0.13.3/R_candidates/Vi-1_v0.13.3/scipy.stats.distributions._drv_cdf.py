def _drv_cdf(self, xk, *args):
    indx = argmax((self.xk > xk),axis=-1)-1
    return self.F[self.xk[indx]]
