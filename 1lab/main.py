import numpy as np
N = 10  
num_shuffles = 1000 
positions = np.zeros((N, N), dtype=int)
for _ in range(num_shuffles):
    arr = np.arange(1, N+1)
    np.random.shuffle(arr)
    for pos, number in enumerate(arr):
        positions[pos, number-1] += 1
for pos in range(N):
    print(f'Позиция {pos+1}:', positions[pos])
