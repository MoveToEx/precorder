from precorder.controller import run
from logging import basicConfig, INFO

basicConfig(level=INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

if __name__ == '__main__':
    run()

