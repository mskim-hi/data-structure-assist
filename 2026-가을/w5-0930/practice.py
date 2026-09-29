# practice.py — 5주차 실습: 정렬 리스트와 비정렬 리스트 비교
#
# 규칙
#  - AI 사용 금지. 직접 채운다.
#  - 파이썬 list의 append / insert / remove / index / in / sort 사용 금지.
#    bisect 모듈도 사용 금지.
#    self.data(고정 크기 배열)와 self.length만 직접 조작한다.
#  - NEED_TO_SOLVE는 아무 동작도 하지 않는 빈 자리다.
#    (실행은 되지만, 그대로 두면 결과가 틀린다.)
#
# 실행: python3 practice.py

import time

MAX_SIZE = 100

NEED_TO_SOLVE = None  # TODO: 이 자리를 직접 채우세요


class UnsortedList:
    """4주차에 만든 비정렬 리스트. 이번 주는 비교 기준으로만 쓴다 (그대로 주어짐)."""

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
    """배열(고정 크기)로 구현한 정렬 리스트.

    data[0] ~ data[length-1]은 항상 오름차순으로 유지된다.
    이 약속을 지키는 대신, findItem을 이진 탐색으로 만들 수 있다.
    """

    def __init__(self, max_size=MAX_SIZE):
        self.data = [None] * max_size   # 저장 공간 (크기 고정)
        self.length = 0                 # 지금 들어 있는 원소 개수
        self.max_size = max_size

    # =======================================================================
    # 관찰자 (Observer) — 값을 바꾸지 않는 연산. 직접 채울 것은 없다.
    # data[0] ~ data[length-1]만 의미 있는 값이고 그 뒤는 쓰레기 값이다.
    # =======================================================================
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

    # =======================================================================
    # 문제 1. insertItem — 정렬 순서를 지키며 삽입한다
    #
    #   [1, 4, 5]에 insertItem(3) -> [1, 3, 4, 5]
    #   ① 들어갈 위치 탐색 (앞에서부터, data[i] >= value가 되는 첫 자리)
    #   ② 그 위치부터 뒤에서부터 한 칸씩 밀기 (4주차 insertItem과 같은 방식)
    #   ③ 빈 자리에 값 쓰기 + length 증가
    # =======================================================================
    def insertItem(self, value):
        if self.isFull():
            raise OverflowError("List is full")

        # 1) 위치 찾기: data[location] >= value가 되는 첫 위치
        location = 0
        while NEED_TO_SOLVE:
            location += 1

        # 2) location부터 끝까지, 뒤에서부터 오른쪽으로 한 칸씩 밀기
        i = self.size()
        while NEED_TO_SOLVE:
            NEED_TO_SOLVE
            i -= 1

        # 3) 삽입
        NEED_TO_SOLVE = value
        self.length += 1

    # =======================================================================
    # 문제 2. findItem — 이진 탐색. 찾으면 위치, 없으면 -1을 반환한다
    #
    #   정렬되어 있으므로 가운데 값과 비교해서 탐색 범위를 반씩 줄인다.
    #   4주차 findItem(선형 탐색, 앞에서부터 하나씩)과 비교해볼 것.
    # =======================================================================
    def findItem(self, item):
        first, last = NEED_TO_SOLVE, NEED_TO_SOLVE
        while NEED_TO_SOLVE:
            mid = NEED_TO_SOLVE

            if NEED_TO_SOLVE:
                NEED_TO_SOLVE
            elif NEED_TO_SOLVE:
                NEED_TO_SOLVE
            else:
                return mid

        return -1

    # =======================================================================
    # 문제 3. removeItem — 값을 찾아서 지운다. 지웠으면 True, 없으면 False
    #
    #   ① findItem으로 위치 찾기 (없으면 False)
    #   ② 그 위치부터 끝까지 한 칸씩 왼쪽으로 당기기
    #      (4주차처럼 맨 뒤 값으로 덮어쓰면 순서가 깨진다. 반드시 당겨야 한다.)
    #   ③ 마지막 자리를 비우고 length 감소
    # =======================================================================
    def removeItem(self, value):
        if self.isEmpty():
            return False

        idx = self.findItem(value)
        if idx == -1:
            return False

        # idx 이후를 한 칸씩 왼쪽으로 당김
        i = idx
        while NEED_TO_SOLVE:
            NEED_TO_SOLVE
            i += 1

        # 꼬리 정리
        self.data[self.size() - 1] = None
        self.length -= 1
        return True

    # =======================================================================
    # 문제 4. updateItem — 값을 바꾸되 정렬 순서를 유지한다
    #
    #   data[pos]를 새 값으로 그냥 덮어쓰면 순서가 깨질 수 있다.
    #   (예: [1, 3, 5]에서 3을 9로 바꾸면 [1, 9, 5] -> 정렬이 아니다.)
    #   그래서 old_value를 지우고, new_value를 다시 정렬 위치에 넣는다.
    # =======================================================================
    def updateItem(self, old_value, new_value):
        removed = NEED_TO_SOLVE
        if not removed:
            return False
        NEED_TO_SOLVE
        return True


# ===========================================================================
# 체크포인트 — 구현이 맞는지 확인한다 (수정하지 않아도 됨)
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
# 문제 5. 정렬 vs 비정렬 비교 실험 (코드는 주어진다. 결과를 읽고 해석한다)
#
#  - 실험 1: 값이 없는 경우를 찾는다. SortedList(이진 탐색) vs UnsortedList(선형 탐색)
#  - 실험 2: 새 값 하나를 넣는다. SortedList(순서를 지키며 삽입) vs UnsortedList(그냥 뒤에 붙임)
#  - 볼 것: 정렬 리스트가 이기는 연산과, 비정렬 리스트가 이기는 연산이 서로 다르다.
# ===========================================================================
def build_sorted(n, extra=10):
    """0 ~ n-1을 순서대로 채운다. (이미 정렬된 값이라 insertItem 없이 직접 채움)"""
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
    """없는 값(-1)을 찾는다. 둘 다 최악의 경우(끝까지 가야 확인됨)."""
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
    """항상 지금까지 넣은 값보다 작은 값을 삽입한다.

    SortedList: 맨 앞자리로 정해지므로(위치 탐색은 즉시 끝) N개를 전부 한 칸씩 밀어야 한다.
    UnsortedList: 순서가 필요 없으므로 그냥 뒤에 붙이면 끝난다.
    """
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

    print("생각해보기")
    print("  1. 실험 1과 실험 2에서, 정렬 리스트가 이기는 연산과 비정렬 리스트가 이기는 연산은?")
    print("  2. 삽입은 잦고 탐색은 드문 상황이라면 어느 쪽을 쓰겠는가?")
    print("  3. removeItem은 findItem(문제 2) + 당기기(문제 3)로 되어 있다. 무엇이 Big-O를 결정하는가?")


if __name__ == "__main__":
    if run_checks():
        run_experiment()
    else:
        print("체크포인트를 먼저 통과시킨 뒤 실험을 돌린다.")
