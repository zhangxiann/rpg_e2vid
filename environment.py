import platform
import os



#  如果是 Windows
if platform.platform().startswith("Windows"):
    source_n_mnist_dir = 'data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = 'data/input/N-MNIST/txt/Test'

    source_n_cars_dir = 'data/input/n_cars'
    target_n_cars_dir = 'data/input/n_cars'

else: # 如果是 Linux
    source_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/bin/Test'
    target_n_mnist_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/N-MNIST/txt/Test'

    source_n_cars_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/n_cars'
    target_n_cars_dir = '/home/jt/HEU_ZX/rpg_e2vid/data/input/n_cars'

n_cars_train_test = ['n_cars_train', 'n_cars_test']