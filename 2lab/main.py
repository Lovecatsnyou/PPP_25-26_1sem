from collections import Counter
def map_letters_by_frequency(s1, s2):
    freq1 = Counter(s1)
    freq2 = Counter(s2)
    letters1 = {}
    letters2 = {}
    for k, v in freq1.items():
        letters1.setdefault(v, []).append(k)
    for k, v in freq2.items():
        letters2.setdefault(v, []).append(k)
    freq_pairs = sorted(set(letters1) & set(letters2), reverse=True)
    mapping = []
    for freq in freq_pairs:
        l1 = sorted(letters1[freq])
        l2 = sorted(letters2[freq])
        if len(l1) != len(l2):
            return "Некорректное отображение: неоднозначные частоты или недостаток символов."
        for x, y in zip(l1, l2):
            mapping.append(f"{x}={y}")
    unmapped_freq1 = set(letters1) - set(letters2)
    unmapped_freq2 = set(letters2) - set(letters1)
    if unmapped_freq1 or unmapped_freq2:
        return "Некорректное отображение: несовпадающие частоты символов."
    return " ".join(mapping)
input1 = "abcbaa"
input2 = "jkekjj"
output = map_letters_by_frequency(input1, input2)
print(output)
