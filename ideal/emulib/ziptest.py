from itertools import zip_longest

one = [1, 2, 3, 4, 5, 6]
two = ["a", "b", "c", "d"]

for i in zip_longest(one, two):
    print(i)

