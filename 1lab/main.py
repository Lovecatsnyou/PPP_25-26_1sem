

if __name__ == "__main__":
    pass # Ваш код здесь
import random
from collections import defaultdic
N = 10        
trials = 1000
counts = [defaultdict(int) for _ in range(N)]
for _ in range(trials):
    arr = list(range(1, N + 1))
    random.shuffle(arr)  
    for i, num in enumerate(arr):
        counts[i][num] += 1
print(f"Результаты после {trials} тасовок:\n")
for i in range(N):
    print(f"Позиция {i + 1}:")
    for num in range(1, N + 1):
        freq = counts[i][num] / trials
        print(f"  Число {num}: {freq:.3f}")
    print()
