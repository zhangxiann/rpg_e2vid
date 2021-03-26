import platform
import os



#  如果是 Windows
if platform.platform().startswith("Windows"):
    source_n_mnist_dir = 'data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = 'data/input/N-MNIST/txt/Test'

    source_n_cars_dir = 'data/input/n_cars/dat'
    target_n_cars_dir = 'data/input/n_cars/txt'

else: # 如果是 Linux
    source_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/txt/Test'

    source_n_cars_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/n_cars/txt'
    target_n_cars_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/n_cars/txt'

n_cars_train_test = ['n-cars_train', 'n-cars_test']