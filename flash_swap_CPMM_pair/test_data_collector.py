from flash_swap.initializer import (
    Initializer
)

init = Initializer('sepolia', 5)

init.initialize_data_collector()
dc = init.data_collector


