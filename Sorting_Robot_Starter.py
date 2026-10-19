"""CSC 225 — Sorting Robot Lottery, simplified edition.

Complete TimeSheet, choose_algorithms, and only your two randomly assigned sorts.
Each sorting function returns (sorted_original_list, number_of_value_comparisons).
Run: python3 Sorting_Robot_Starter.py
"""
import random


class TimeSheet:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.comparisons = []

    def add_run(self, count):
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("Count must be a nonnegative interger")
        self.comparisons.append(count)

    def average(self):
        if len(self.comparisons) == 0:
            return None
        return sum(self.comparisons) / len(self.comparisons)

    def median(self):
        if len(self.comparisons) == 0:
            return None

        numbers = sorted(self.comparisons)
        middle = len(numbers) // 2

        if len(numbers) % 2 == 1:
            return numbers[middle]
        else:
            return (numbers[middle - 1] + numbers[middle]) / 2

    def standard_deviation(self):
        if len(self.comparisons) == 0:
            return None

        mean = self.average()
        total = 0

        for count in self.comparisons:
            total += (count - mean) ** 2

        variance = total / len(self.comparisons)
        return variance ** 0.5


    def minimum(self):
        if len(self.comparisons) == 0:
            return None
        return min(self.comparisons)

    def maximum(self):
        if len(self.comparisons) == 0:
            return None
        return max(self.comparisons)


    
def bubble_sort(values):
    comparisons = 0
    n = len(values)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            comparisons += 1

            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
                swapped = True

        if not swapped:
            break

    return values, comparisons



    
def selection_sort(values):
    comparisons = 0
    n = len(values)

    for i in range(n - 1):
        small = i

        for j in range(i + 1, n):
            comparisons += 1

            if values[j] < values[small]:
                small = j

        values[i], values[small] = values[small], values[i]

    return values, comparisons


    
def merge_sort(values):
    n = len(values)

    if n <= 1:
        return values, 0

    mid = n // 2

    left, left_count = merge_sort(values[:mid])
    right, right_count = merge_sort(values[mid:])

    new = []
    i = 0
    j = 0
    comparisons = left_count + right_count

    while i < len(left) and j < len(right):
        comparisons += 1

        if left[i] < right[j]:
            new.append(left[i])
            i += 1
        else:
            new.append(right[j])
            j += 1

    new += left[i:] + right[j:]

    return new, comparisons




def quick_sort(values):
    n = len(values)

    if n <= 1:
        return values, 0

    pivot = values[-1]
    small = []
    big = []
    comparisons = 0

    for i in values[:-1]:
        comparisons += 1

        if i <= pivot:
            small.append(i)
        else:
            big.append(i)

    sorted_small, small_count = quick_sort(small)
    sorted_big, big_count = quick_sort(big)

    total_comparisons = comparisons + small_count + big_count

    return sorted_small + [pivot] + sorted_big, total_comparisons



def heap_sort(values):
    comparisons = 0
    n = len(values)

    def sift_down(root, end):
        nonlocal comparisons

        while 2 * root + 1 < end:
            child = 2 * root + 1

            if child + 1 < end:
                comparisons += 1
                if values[child + 1] > values[child]:
                    child += 1

            comparisons += 1
            if values[root] >= values[child]:
                break

            values[root], values[child] = values[child], values[root]
            root = child

    
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    for end in range(n - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        sift_down(0, end)

    return values, comparisons

ALGORITHMS = {
    "Bubble": bubble_sort,
    "Selection": selection_sort,
    "Merge": merge_sort,
    "Quick": quick_sort,
    "Heap": heap_sort,
}


def choose_algorithms(seed):
    rng = random.Random(seed)
    return rng.sample(list(ALGORITHMS.keys()), 2)


NUMBER_OF_RUNS = 50
LIST_SIZE = 100


def make_test_lists(seed):
    """Create reproducible random lists; both methods receive identical inputs."""
    rng = random.Random(seed + 1000)
    return [[rng.randint(0, 999) for _ in range(LIST_SIZE)]
            for _ in range(NUMBER_OF_RUNS)]


def run_lab(seed):
    selected = choose_algorithms(seed)
    sheets = {name: TimeSheet(name) for name in selected}
    print(f"Seed: {seed} | Algorithms: {', '.join(selected)}")
    print(f"{'Run':>4} {'Method':12} {'Comparisons':>12}")
    for run_number, original in enumerate(make_test_lists(seed), start=1):
        for name in selected:
            values = original.copy()
            _, count = ALGORITHMS[name](values)
            sheets[name].add_run(count)
            print(f"{run_number:4d} {name:12} {count:12d}")
    print("\nCOMPARISON SUMMARIES")
    for name in selected:
        sheet = sheets[name]
        print(f"{name}: counts={sheet.comparisons}, average={sheet.average()}, "
              f"median={sheet.median()}, std_dev={sheet.standard_deviation()}, "
              f"min={sheet.minimum()}, max={sheet.maximum()}")


if __name__ == "__main__":
    seed = int(input("Enter your integer seed: "))
    run_lab(seed)
