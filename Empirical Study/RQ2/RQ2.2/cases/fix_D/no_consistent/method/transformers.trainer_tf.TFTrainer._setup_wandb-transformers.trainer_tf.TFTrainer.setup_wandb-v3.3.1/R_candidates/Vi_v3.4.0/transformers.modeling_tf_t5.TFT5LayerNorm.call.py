    def call(self, x):
        variance = tf.math.reduce_mean(tf.math.square(x), axis=-1, keepdims=True)
        x = x * tf.math.rsqrt(variance + self.variance_epsilon)
        return self.weight * x
