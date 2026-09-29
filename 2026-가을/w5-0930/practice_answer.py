# practice_answer.py — 5주차 실습 정답: 정렬 리스트와 비정렬 리스트 비교
#
# 실행: python3 practice_answer.py

import time

MAX_SIZE = 100


class UnsortedList:
    """4주차에 만든 비정렬 리스트. 이번 주는 비교 기준으로만 쓴다."""

    def __init__(self, max_size=MAX_SIZE):
        self.data = [None] * max_size
        self.length = 0
        self.max_size = max_size

    def size(self):
        return self.length

    def isFull(self):
        return self.length == self.max_size

    def isEmpty(self):
        return self.length == 0

    def getItem(self, pos):
        if pos < 0 or pos >= self.length:
            raise IndexError("pos out of range")
        return self.data[pos]

    def clear(self):
        self.length = 0

    def toList(self):
        return [self.data[i] for i in range(self.length)]

    def appendItem(self, value):
        if self.isFull():
            raise OverflowError("List is full")
        self.data[self.length] = value
        self.length += 1

    def findItem(self, item):
        pos = 0
        while pos < self.length:
            if self.data[pos] == item:
                return pos
            pos += 1
        return -1


class SortedList:
    """배열(고정 크기)로 구현한 정렬 리스트. data[0..length-1]은 항상 오름차순."""

    def __init__(self, max_size=MAX_SIZE):
        self.data = [None] * max_size
        self.length = 0
        self.max_size = max_size

    # ===== 관찰자 (Observer) — 값을 바꾸지 않는 연산 =====
    def size(self):
        return self.length

    def isFull(self):
        return self.length == self.max_size

    def isEmpty(self):
        return self.length == 0

    def getItem(self, pos):
        if pos < 0 or pos >= self.length:
            raise IndexError("pos out of range")
        return self.data[pos]

    def clear(self):
        self.length = 0

    def toList(self):
        return [self.data[i] for i in range(self.length)]

    # ===== 문제 1. insertItem — 정렬 순서를 지키며 삽입 =====
    def insertItem(self, value):
        if self.isFull():
            raise OverflowError("List is full")

        location = 0
        while location < self.size() and self.data[location] < value:
            location += 1

        i = self.size()
        while i > location:
            self.data[i] = self.data[i - 1]
            i -= 1

        self.data[location] = value
        self.length += 1

    # ===== 문제 2. findItem — 이진 탐색 (O(log N)) =====
    def findItem(self, item):
        first, last = 0, self.size() - 1
        while first <= last:
            mid = (first + last) // 2

            if item < self.data[mid]:
                last = mid - 1
            elif item > self.data[mid]:
                first = mid + 1
            else:
                return mid

        return -1

    # ===== 문제 3. removeItem — 찾아서 지우고, 왼쪽으로 당겨서 메움 =====
    def removeItem(self, value):
        if self.isEmpty():
            return False

        idx = self.findItem(value)
        if idx == -1:
            return False

        i = idx
        while i < self.size() - 1:
            self.data[i] = self.data[i + 1]
            i += 1

        self.data[self.size() - 1] = None
        self.length -= 1
        return True

    # ===== 문제 4. updateItem — 지우고 다시 정렬 위치에 삽입 =====
    def updateItem(self, old_value, new_value):
        removed = self.removeItem(old_value)
        if not removed:
            return False
        self.insertItem(new_value)
        return True


# ===========================================================================
# 체크포인트 (수정하지 않아도 됨)
# ===========================================================================
def make(values, max_size=MAX_SIZE):
    lst = SortedList(max_size)
    for v in values:
        lst.insertItem(v)
    return lst


def removed(lst, value):
    return (lst.removeItem(value), lst.toList())


def updated(lst, old_value, new_value):
    return (lst.updateItem(old_value, new_value), lst.toList())


CASES = [
    ("insertItem 3,5,1,4,2 삽입", lambda: make([3, 5, 1, 4, 2]).toList(),          [1, 2, 3, 4, 5]),
    ("findItem(4)",               lambda: make([3, 5, 1, 4, 2]).findItem(4),        3),
    ("findItem(10)",              lambda: make([3, 5, 1, 4, 2]).findItem(10),       -1),
    ("removeItem(3)",             lambda: removed(make([3, 5, 1, 4, 2]), 3),        (True, [1, 2, 4, 5])),
    ("removeItem(10)",            lambda: removed(make([3, 5, 1, 4, 2]), 10),       (False, [1, 2, 3, 4, 5])),
    ("updateItem(3, 10)",         lambda: updated(make([3, 5, 1, 4, 2]), 3, 10),    (True, [1, 2, 4, 5, 10])),
    ("updateItem(99, 1)",         lambda: updated(make([3, 5, 1, 4, 2]), 99, 1),    (False, [1, 2, 3, 4, 5])),
]


def run_checks():
    print("=== 체크포인트 ===")
    ok = True
    for name, fn, expected in CASES:
        try:
            got = fn()
        except Exception as e:
            got = f"{type(e).__name__}: {e}"
        passed = (got == expected)
        ok = ok and passed
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}: {got}"
              + ("" if passed else f"  (기대: {expected})"))
    print(f"결과: {'전부 통과' if ok else '통과하지 못한 항목이 있다'}\n")
    return ok


# ===========================================================================
# 정렬 vs 비정렬 비교 실험 (수정하지 않아도 됨)
# ===========================================================================
def build_sorted(n, extra=10):
    lst = SortedList(n + extra)
    for i in range(n):
        lst.data[i] = i
    lst.length = n
    return lst


def build_unsorted(n, extra=10):
    lst = UnsortedList(n + extra)
    for i in range(n):
        lst.appendItem(i)
    return lst


def measure_find(n):
    result = []
    for build, method, repeat in ((build_sorted, "findItem", 2000), (build_unsorted, "findItem", 20)):
        lst = build(n)
        f = getattr(lst, method)
        start = time.perf_counter()
        for _ in range(repeat):
            f(-1)
        elapsed = time.perf_counter() - start
        result.append(elapsed / repeat * 1_000_000)
    return result


def measure_insert(n):
    repeat = 300
    lst_s = build_sorted(n, extra=repeat + 10)
    start = time.perf_counter()
    for k in range(repeat):
        lst_s.insertItem(-k - 1)
    sorted_us = (time.perf_counter() - start) / repeat * 1_000_000

    lst_u = build_unsorted(n, extra=repeat + 10)
    start = time.perf_counter()
    for k in range(repeat):
        lst_u.appendItem(-k - 1)
    unsorted_us = (time.perf_counter() - start) / repeat * 1_000_000

    return sorted_us, unsorted_us


def run_experiment():
    print("=== 실험 1. findItem — SortedList(이진 탐색) vs UnsortedList(선형 탐색) ===")
    print("       N | SortedList |  UnsortedList")
    print("-" * 40)
    for n in (1000, 2000, 4000, 8000, 16000):
        sorted_us, unsorted_us = measure_find(n)
        print(f"{n:>8} | {sorted_us:>9.3f}us | {unsorted_us:>11.1f}us")
    print("N이 2배가 되어도 SortedList는 거의 그대로 -> O(log N)")
    print("UnsortedList는 N에 비례해서 커짐 -> O(N)\n")

    print("=== 실험 2. 새 값 삽입 — SortedList(정렬 유지) vs UnsortedList(그냥 append) ===")
    print("       N | SortedList |  UnsortedList")
    print("-" * 40)
    for n in (1000, 2000, 4000, 8000, 16000):
        sorted_us, unsorted_us = measure_insert(n)
        print(f"{n:>8} | {sorted_us:>9.1f}us | {unsorted_us:>11.3f}us")
    print("N이 2배가 되면 SortedList도 약 2배 -> O(N)")
    print("UnsortedList는 N이 커져도 그대로 -> O(1)\n")


if __name__ == "__main__":
    if run_checks():
        run_experiment()
    else:
        print("체크포인트를 먼저 통과시킨 뒤 실험을 돌린다.")
