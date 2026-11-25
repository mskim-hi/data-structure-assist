# practice.py — 12주차 실습: 재귀(피보나치, 메모이제이션)와 우선순위 큐(힙)
#
# 규칙
#  - AI 사용 금지. 직접 채운다.
#  - 직접 채우는 코드에서 functools.lru_cache, heapq, sort / sorted 사용 금지.
#  - NEED_TO_SOLVE는 아무 동작도 하지 않는 빈 자리다.
#    (실행은 되지만, 그대로 두면 결과가 틀린다.)
#
# 실행: python3 practice.py          (전부)
#       python3 practice.py fib      (문제 1~3만)
#       python3 practice.py heap     (문제 4~6만)
#       python3 practice.py sort     (문제 7~9. 실험은 문제 4~6 통과 후)

import math
import random
import sys
import time

MAX_SIZE = 100

NEED_TO_SOLVE = None  # TODO: 이 자리를 직접 채우세요


# ###########################################################################
# PART 1. 재귀 — 피보나치 수열
#
#   fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)
#   0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
# ###########################################################################

# 호출 횟수 기록용 (수정하지 않음)
RECURSIVE_CALLS = {}   # RECURSIVE_CALLS[k] = fib_recursive(k)가 호출된 횟수
MEMO_CALLS = [0]       # fib_memo가 호출된 총 횟수


def reset_counters():
    RECURSIVE_CALLS.clear()
    MEMO_CALLS[0] = 0


# ===========================================================================
# 문제 1. fib_recursive — 정의 그대로 재귀 호출
#
#   재귀 함수 = base case(더 이상 호출하지 않고 바로 답을 냄)
#             + recursive case(더 작은 n으로 자기 자신을 호출)
#   base case가 없으면 호출이 끝나지 않는다 (RecursionError).
# ===========================================================================
def fib_recursive(n):
    RECURSIVE_CALLS[n] = RECURSIVE_CALLS.get(n, 0) + 1   # 호출 기록 (수정하지 않음)

    # TODO 1) base case: n이 0 또는 1이면 n을 그대로 반환
    if NEED_TO_SOLVE:
        return NEED_TO_SOLVE

    # TODO 2) recursive case: fib(n-1) + fib(n-2)
    return NEED_TO_SOLVE


# ===========================================================================
# 문제 2. fib_memo — 한 번 계산한 값은 memo에 저장하고 재사용
#
#   memo: 딕셔너리. memo[k] = fib(k)
#   ① memo에 n이 있으면 계산하지 않고 바로 반환
#   ② 없으면 문제 1과 같은 식으로 계산 (재귀 호출에 같은 memo를 넘김)
#   ③ 계산한 값을 memo[n]에 저장하고 반환
# ===========================================================================
def fib_memo(n, memo=None):
    MEMO_CALLS[0] += 1                                    # 호출 기록 (수정하지 않음)
    if memo is None:
        memo = {}

    # TODO ① 이미 계산한 값이면 바로 반환
    if NEED_TO_SOLVE:
        return NEED_TO_SOLVE

    # TODO ② 계산
    if n <= 1:
        result = n
    else:
        result = NEED_TO_SOLVE

    # TODO ③ 저장하고 반환
    NEED_TO_SOLVE
    return result


# ===========================================================================
# 문제 3. 순수 재귀 vs 메모이제이션 실험 (코드는 주어진다. 결과를 읽고 해석한다)
#
#  - 실험 1-1: fib(5) 한 번 계산할 때 같은 인자가 몇 번 호출되는가
#  - 실험 1-2: n을 2씩 키우며 호출 수와 시간을 비교한다
#  - 실험 1-3: 메모이제이션만 n을 2배씩 키운다
# ===========================================================================
def run_fib_experiment():
    reset_counters()
    fib_recursive(5)
    print("=== 실험 1-1. fib_recursive(5) 안에서 각 인자가 호출된 횟수 ===")
    for k in range(5, -1, -1):
        print(f"  fib({k}) : {RECURSIVE_CALLS.get(k, 0)}회")
    print(f"  합계    : {sum(RECURSIVE_CALLS.values())}회\n")

    print("=== 실험 1-2. fib(n) 1회 계산 — 순수 재귀 vs 메모이제이션 ===")
    print("   n |  재귀 호출 수 |   재귀 시간 | 메모 호출 수 |  메모 시간")
    print("-" * 64)
    for n in (20, 22, 24, 26, 28, 30, 32):
        reset_counters()
        start = time.perf_counter()
        fib_recursive(n)
        rec_ms = (time.perf_counter() - start) * 1000
        rec_calls = sum(RECURSIVE_CALLS.values())

        start = time.perf_counter()
        fib_memo(n)
        memo_ms = (time.perf_counter() - start) * 1000

        print(f"{n:>4} | {rec_calls:>12,} | {rec_ms:>8.1f}ms | {MEMO_CALLS[0]:>11,} | {memo_ms:>7.3f}ms")
    print()

    print("=== 실험 1-3. 메모이제이션만 n을 더 키운다 ===")
    print("   n | 메모 호출 수 |  메모 시간 | fib(n) 자릿수")
    print("-" * 48)
    for n in (100, 200, 400, 800):
        reset_counters()
        start = time.perf_counter()
        value = fib_memo(n)
        memo_ms = (time.perf_counter() - start) * 1000
        print(f"{n:>4} | {MEMO_CALLS[0]:>11,} | {memo_ms:>7.3f}ms | {len(str(value)):>6}")
    print()

    print("생각해보기")
    print("  1. 순수 재귀에서 n이 2 늘 때 호출 수는 몇 배가 되는가?")
    print("  2. 메모이제이션에서 n이 2배가 될 때 호출 수는 몇 배가 되는가?")
    print("  3. fib_recursive(32)를 계산할 때 fib(2)는 몇 번 다시 계산되는가?\n")


# ###########################################################################
# PART 2. 우선순위 큐 — 최대 힙 (Max Heap)
#
#   배열 하나로 완전 이진 트리를 표현한다. (0번 칸이 루트)
#     부모   (i - 1) // 2
#     왼쪽   2 * i + 1
#     오른쪽 2 * i + 2
#   힙 조건: 모든 노드에서 부모 >= 자식  -> 최댓값은 항상 data[0]
# ###########################################################################

def parent(i):
    return (i - 1) // 2


def left(i):
    return 2 * i + 1


def right(i):
    return 2 * i + 2


# ===========================================================================
# 문제 4. sift_up — 새 값을 부모와 비교하며 위로 올린다 (push에서 사용)
#
#   push(7): [9, 3, 2] 맨 뒤에 7 -> [9, 3, 2, 7]
#            7(i=3)의 부모는 3(i=1). 3 < 7 이므로 교환 -> [9, 7, 2, 3]
#            7(i=1)의 부모는 9(i=0). 9 >= 7 이므로 멈춤
# ===========================================================================
def sift_up(data, i):
    # TODO: i가 루트(0)가 아닐 동안 반복
    while NEED_TO_SOLVE:
        p = parent(i)
        # TODO: 부모가 더 크거나 같으면 멈춤
        if NEED_TO_SOLVE:
            break
        # TODO: 부모와 자리를 바꾸고, i를 부모 자리로 옮긴다
        NEED_TO_SOLVE
        i = NEED_TO_SOLVE


# ===========================================================================
# 문제 5. sift_down — 루트에 온 값을 더 큰 자식과 비교하며 아래로 내린다
#                     (pop과 heap_sort에서 사용)
#
#   size: 힙으로 쓰는 범위. data[0] ~ data[size-1]만 본다.
#
#   pop(): [9, 7, 2, 3, 5] 에서 9를 꺼내고 맨 뒤 5를 루트로 -> [5, 7, 2, 3]
#          5(i=0)의 자식 7, 2 중 큰 쪽 7과 비교. 5 < 7 이므로 교환 -> [7, 5, 2, 3]
#          5(i=1)의 자식 3 하나. 5 >= 3 이므로 멈춤
# ===========================================================================
def sift_down(data, i, size):
    while True:
        l, r = left(i), right(i)

        # TODO 1) 자식이 하나도 없으면 멈춤 (왼쪽 자식 인덱스가 size 이상)
        if NEED_TO_SOLVE:
            break

        # TODO 2) 두 자식 중 더 큰 쪽 고르기 (오른쪽 자식은 없을 수도 있음)
        bigger = l
        if NEED_TO_SOLVE:
            bigger = r

        # TODO 3) 내가 더 크거나 같으면 멈춤, 아니면 바꾸고 내려감
        if NEED_TO_SOLVE:
            break
        NEED_TO_SOLVE
        i = NEED_TO_SOLVE


class MaxHeap:
    """배열(고정 크기)로 구현한 최대 힙. 우선순위 큐로 쓴다 (큰 값이 먼저 나옴)."""

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

    def peek(self):
        if self.isEmpty():
            raise IndexError("Heap is empty")
        return self.data[0]

    def toList(self):
        return [self.data[i] for i in range(self.length)]

    # 문제 4. push — 맨 뒤에 넣고 sift_up
    def push(self, value):
        if self.isFull():
            raise OverflowError("Heap is full")
        self.data[self.length] = value
        self.length += 1
        # TODO: 방금 넣은 칸의 인덱스부터 sift_up
        sift_up(self.data, NEED_TO_SOLVE)

    # 문제 5. pop — 루트를 꺼내고, 맨 뒤 값을 루트로 올린 뒤 sift_down
    def pop(self):
        if self.isEmpty():
            raise IndexError("Heap is empty")
        # TODO: 루트(최댓값)를 꺼내 둔다
        top = NEED_TO_SOLVE
        self.length -= 1
        # TODO: 맨 뒤 값(인덱스 length)을 루트로 옮긴다
        self.data[0] = NEED_TO_SOLVE
        self.data[self.length] = None
        # TODO: 루트부터, 줄어든 길이 범위 안에서 sift_down
        sift_down(self.data, NEED_TO_SOLVE, NEED_TO_SOLVE)
        return top


# ###########################################################################
# PART 3. 힙 정렬 (Heap Sort)
# ###########################################################################

# ===========================================================================
# 문제 6. heap_sort — 배열 자체를 힙으로 만든 뒤, 최댓값을 맨 뒤로 보내기를 반복
#
#   ① 힙 만들기: 마지막 내부 노드(n//2 - 1)부터 0까지 거꾸로 sift_down
#      (n//2 이후는 자식이 없는 노드라 sift_down 할 필요가 없다)
#   ② 정렬: end = n-1 ~ 1
#        arr[0](최댓값)과 arr[end]를 바꾸고, 0 ~ end-1 범위로 sift_down
#   새 배열을 만들지 않는다. arr 안에서만 자리를 바꾼다.
# ===========================================================================
def heap_sort(arr):
    n = len(arr)

    # TODO ① 힙 만들기: i = n//2 - 1, ..., 1, 0
    for i in range(NEED_TO_SOLVE, -1, -1):
        NEED_TO_SOLVE

    # TODO ② end = n-1, ..., 2, 1
    for end in range(NEED_TO_SOLVE, 0, -1):
        NEED_TO_SOLVE      # arr[0]과 arr[end] 교환
        NEED_TO_SOLVE      # 0 ~ end-1 범위로 sift_down

    return arr


# ===========================================================================
# 비교용 정렬 (이론 시간에 배운 정렬. 그대로 주어짐)
# ===========================================================================
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if arr[j] < arr[m]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    a = merge_sort(arr[:mid])
    b = merge_sort(arr[mid:])
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


# ###########################################################################
# PART 4. 정렬 비교 — 비교 횟수로 시간 복잡도 확인
#
#   실행 시간은 컴퓨터마다 다르다. 비교 횟수는 어디서 돌려도 같다.
#   정렬은 "두 값 비교"가 기본 연산 -> 비교 횟수가 N에 따라 어떻게 느는지 = 시간 복잡도
# ###########################################################################

# 비교 횟수 기록용 (수정하지 않음)
COMPARES = [0]


class Num:
    """정수 하나를 감싼 값. <, >, <=, >= 비교를 할 때마다 COMPARES[0]이 1 늘어난다.
    정렬 코드는 고치지 않고, 값만 Num으로 바꿔 넣으면 비교 횟수를 셀 수 있다."""

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        COMPARES[0] += 1
        return self.v < other.v

    def __gt__(self, other):
        COMPARES[0] += 1
        return self.v > other.v

    def __le__(self, other):
        COMPARES[0] += 1
        return self.v <= other.v

    def __ge__(self, other):
        COMPARES[0] += 1
        return self.v >= other.v


def count_compares(sort_fn, values):
    """values를 sort_fn으로 정렬할 때의 비교 횟수 (정렬 결과도 확인)"""
    arr = [Num(v) for v in values]
    COMPARES[0] = 0
    result = sort_fn(arr)
    assert [x.v for x in result] == sorted(values), f"{sort_fn.__name__} 결과가 틀림"
    return COMPARES[0]


def make_input(kind, n, seed=0):
    """kind: 'sorted' (오름차순) / 'reversed' (내림차순) / 'random' (무작위)"""
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n - 1, -1, -1))
    rng = random.Random(seed)
    return [rng.randint(0, 100000) for _ in range(n)]


# ===========================================================================
# 문제 7. 비교 횟수 공식 — 코드를 보고 비교 횟수를 N에 대한 식으로 쓴다
#
#   위 selection_sort, insertion_sort 코드에서 arr[j] < arr[m], arr[j] > key 가
#   몇 번 실행되는지 센다. (n >= 1)
#
#   ① selection_compares(n)          : 입력과 상관없이 항상 같다
#        i = 0일 때 안쪽 for는 몇 번? i = 1일 때는? ... 마지막 i = n-2일 때는?
#   ② insertion_compares_sorted(n)   : 이미 정렬된 입력 [0, 1, ..., n-1]
#        arr[j] > key 가 처음부터 거짓 -> while을 바로 빠져나감
#   ③ insertion_compares_reversed(n) : 역순 입력 [n-1, ..., 1, 0]
#        key가 매번 맨 앞까지 이동. j가 -1이 되면 j >= 0 에서 멈춰 arr[j] > key는 실행 안 됨
#
#   정수 나눗셈은 // 를 쓴다. (예: 10 * 9 // 2 = 45)
# ===========================================================================
def selection_compares(n):
    # TODO ①
    return NEED_TO_SOLVE


def insertion_compares_sorted(n):
    # TODO ②
    return NEED_TO_SOLVE


def insertion_compares_reversed(n):
    # TODO ③
    return NEED_TO_SOLVE


# ===========================================================================
# 체크포인트 — 구현이 맞는지 확인한다 (수정하지 않아도 됨)
# ===========================================================================
def calls_of_fib5():
    reset_counters()
    fib_recursive(5)
    return (RECURSIVE_CALLS.get(2, 0), sum(RECURSIVE_CALLS.values()))


def memo_calls(n):
    reset_counters()
    value = fib_memo(n)
    return (value, MEMO_CALLS[0])


def make_heap(values):
    h = MaxHeap()
    for v in values:
        h.push(v)
    return h


def pop_all(h):
    out = []
    while not h.isEmpty():
        out.append(h.pop())
    return out


def pop_once(h):
    return (h.pop(), h.toList())


def random_sort_ok():
    rng = random.Random(13)
    arr = [rng.randint(0, 999) for _ in range(200)]
    return heap_sort(arr[:]) == sorted(arr)


FIB_CASES = [
    ("문제1 fib_recursive(0), (1), (10)", lambda: (fib_recursive(0), fib_recursive(1), fib_recursive(10)), (0, 1, 55)),
    ("문제1 fib(5) 안에서 fib(2) 호출 수, 총 호출 수", calls_of_fib5,                                      (3, 15)),
    ("문제2 fib_memo(10) 값, 호출 수",     lambda: memo_calls(10),                                       (55, 19)),
    ("문제2 fib_memo(50)",                lambda: fib_memo(50),                                         12586269025),
]

HEAP_CASES = [
    ("문제4 push 3,9,2,7,5",        lambda: make_heap([3, 9, 2, 7, 5]).toList(),           [9, 7, 2, 3, 5]),
    ("문제4 peek",                  lambda: make_heap([3, 9, 2, 7, 5]).peek(),             9),
    ("문제5 pop 1회",               lambda: pop_once(make_heap([3, 9, 2, 7, 5])),          (9, [7, 5, 2, 3])),
    ("문제5 pop 반복",              lambda: pop_all(make_heap([3, 9, 2, 7, 5])),           [9, 7, 5, 3, 2]),
    ("문제6 heap_sort([5,1,4,2,8,3])", lambda: heap_sort([5, 1, 4, 2, 8, 3]),              [1, 2, 3, 4, 5, 8]),
    ("문제6 heap_sort([])",          lambda: heap_sort([]),                                []),
    ("문제6 heap_sort 무작위 200개", random_sort_ok,                                       True),
]


def formula_vs_count(formula, sort_fn, kind):
    return [(formula(n), count_compares(sort_fn, make_input(kind, n))) for n in (1, 10, 100)]


def formula_ok(formula, sort_fn, kind):
    pairs = formula_vs_count(formula, sort_fn, kind)
    return all(f == c for f, c in pairs)


SORT_CASES = [
    ("문제7 selection_compares  (공식, 측정) N=1,10,100",
     lambda: formula_vs_count(selection_compares, selection_sort, "random"),
     [(0, 0), (45, 45), (4950, 4950)]),
    ("문제7 selection_compares 정렬/역순 입력도 같은가",
     lambda: formula_ok(selection_compares, selection_sort, "sorted")
             and formula_ok(selection_compares, selection_sort, "reversed"),
     True),
    ("문제7 insertion_compares_sorted   (공식, 측정)",
     lambda: formula_vs_count(insertion_compares_sorted, insertion_sort, "sorted"),
     [(0, 0), (9, 9), (99, 99)]),
    ("문제7 insertion_compares_reversed (공식, 측정)",
     lambda: formula_vs_count(insertion_compares_reversed, insertion_sort, "reversed"),
     [(0, 0), (45, 45), (4950, 4950)]),
]


def run_checks(title, cases):
    print(f"=== 체크포인트 ({title}) ===")
    ok = True
    for name, fn, expected in cases:
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
# 문제 8. 실험 — 무작위 입력, N을 2배씩 (코드는 주어진다. 결과를 읽고 해석한다)
#
#  - 8-1. 실행 시간  8-2. 비교 횟수  8-3. 비교 횟수 / 기준식
#  - 볼 것: N이 2배가 될 때 시간, 비교 횟수가 몇 배가 되는가.
# ===========================================================================
SORTS = (("selection", selection_sort), ("insertion", insertion_sort),
         ("merge", merge_sort), ("heap", heap_sort))


def run_random_experiment():
    header = "       N | " + " | ".join(f"{name:>10}" for name, _ in SORTS)

    print("=== 실험 8-1. 무작위 정수 N개 정렬 시간 ===")
    print(header)
    print("-" * len(header))
    for n in (1000, 2000, 4000):
        arr = make_input("random", n)
        cells = []
        for _, fn in SORTS:
            start = time.perf_counter()
            result = fn(arr[:])
            ms = (time.perf_counter() - start) * 1000
            assert result == sorted(arr)
            cells.append(f"{ms:>8.1f}ms")
        print(f"{n:>8} | " + " | ".join(cells))
    print()

    print("=== 실험 8-2. 무작위 정수 N개 정렬 — 비교 횟수 ===")
    print(header)
    print("-" * len(header))
    counts = {}
    for n in (1000, 2000, 4000):
        arr = make_input("random", n)
        counts[n] = [count_compares(fn, arr) for _, fn in SORTS]
        print(f"{n:>8} | " + " | ".join(f"{c:>10,}" for c in counts[n]))
    print()

    print("=== 실험 8-3. 비교 횟수 / 기준식 ===")
    print("       N |  sel / N²  |  ins / N²  | merge / NlogN | heap / NlogN")
    print("-" * 64)
    for n, (sel, ins, mer, hp) in counts.items():
        nlogn = n * math.log2(n)
        print(f"{n:>8} | {sel / n ** 2:>9.3f}  | {ins / n ** 2:>9.3f}  |"
              f" {mer / nlogn:>12.3f}  | {hp / nlogn:>11.3f}")
    print("  (logN = log₂N)\n")

    print("생각해보기")
    print("  1. N이 2배가 될 때 selection / insertion 비교 횟수는 몇 배가 되는가?")
    print("  2. N이 2배가 될 때 merge / heap 비교 횟수는 몇 배가 되는가?")
    print("  3. 8-3에서 비율이 N과 상관없이 거의 일정하다는 것은 무엇을 뜻하는가?")
    print("  4. merge와 heap은 둘 다 O(N log N)인데 heap이 더 느린 이유를 8-3에서 찾아라.\n")


# ===========================================================================
# 문제 9. 실험 — 입력 모양에 따른 차이 (코드는 주어진다. 결과를 읽고 해석한다)
#
#  - 같은 N = 2000개를 정렬됨 / 역순 / 무작위 세 가지로 넣는다.
#  - 볼 것: 입력 모양이 바뀌면 비교 횟수가 달라지는 정렬은 어느 것인가.
# ===========================================================================
def run_shape_experiment():
    n = 2000
    kinds = (("sorted", "정렬됨"), ("reversed", "역순"), ("random", "무작위"))
    inputs = {kind: make_input(kind, n) for kind, _ in kinds}
    header = "           |     정렬됨 |       역순 |     무작위"

    print(f"=== 실험 9-1. N = {n} 입력 모양별 비교 횟수 ===")
    print(header)
    print("-" * 52)
    for name, fn in SORTS:
        cells = [f"{count_compares(fn, inputs[kind]):>10,}" for kind, _ in kinds]
        print(f" {name:<9} | " + " | ".join(cells))
    print()

    print(f"=== 실험 9-2. N = {n} 입력 모양별 시간 ===")
    print(header)
    print("-" * 52)
    for name, fn in SORTS:
        cells = []
        for kind, _ in kinds:
            arr = inputs[kind]
            start = time.perf_counter()
            fn(arr[:])
            cells.append(f"{(time.perf_counter() - start) * 1000:>8.1f}ms")
        print(f" {name:<9} | " + " | ".join(cells))
    print()

    print("생각해보기")
    print("  1. 입력 모양과 상관없이 비교 횟수가 같은 정렬은? 문제 7의 공식과 맞는가?")
    print("  2. insertion은 정렬됨 / 역순에서 각각 몇 번 비교하는가? (최선 / 최악)")
    print("  3. heap은 세 입력에서 비교 횟수가 얼마나 차이 나는가?")
    print("  4. 거의 정렬된 데이터가 자주 들어온다면 어떤 정렬을 고르겠는가?")


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"

    if part in ("all", "fib"):
        if run_checks("PART 1 재귀", FIB_CASES):
            run_fib_experiment()
        else:
            print("PART 1 체크포인트를 먼저 통과시킨 뒤 실험을 돌린다.\n")

    heap_ok = True
    if part in ("all", "heap", "sort"):
        heap_ok = run_checks("PART 2~3 힙", HEAP_CASES)

    if part in ("all", "sort"):
        formula_ok_all = run_checks("PART 4 비교 횟수 공식", SORT_CASES)
        if heap_ok and formula_ok_all:
            run_random_experiment()
            run_shape_experiment()
        else:
            print("PART 2~4 체크포인트를 모두 통과시킨 뒤 실험(문제 8, 9)을 돌린다.")
