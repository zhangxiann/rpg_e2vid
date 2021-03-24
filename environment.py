import platform
import os



#  如果是 Windows
if platform.platform().startswith("Windows"):
    source_n_mnist_dir = 'data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = 'data/input/N-MNIST/txt/Test'

else: # 如果是 Linux
    source_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/txt/Test'