import tensorflow as tf
import inspect
from tensorflow.python.keras.callbacks import BackupAndRestore

def main():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu', input_shape=(5,)),
        tf.keras.layers.Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')

    backup_restore_callback = BackupAndRestore(backup_dir='./backup')
    print("BackupAndRestore callback created:", backup_restore_callback)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BackupAndRestore))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
