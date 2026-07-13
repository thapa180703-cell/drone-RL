def list_sum(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total

print("合計:",list_sum([1,2,3,4]))
