# practice.py — 7주차 실습: 스택과 큐 (후위수식 계산기, 원형 큐 링버퍼)
#
# 규칙
#  - AI 사용 금지. 직접 채운다.
#  - 파이썬 list의 append / pop / insert, collections.deque, queue 모듈 사용 금지.
#    self.data(고정 크기 배열)와 top / front / rear 인덱스만 직접 조작한다.
#  - NEED_TO_SOLVE는 아무 동작도 하지 않는 빈 자리다.
#    (실행은 되지만, 그대로 두면 결과가 틀린다.)
#
# 실행: python3 practice.py

import time

MAX_SIZE = 100

NEED_TO_SOLVE = None  # TODO: 이 자리를 직접 채우세요


class ArrayStack:
    """배열(고정 크기)로 구현한 스택. top은 맨 위 원소의 인덱스 (-1이면 비어 있음)."""

    def __init__(self, max_size=MAX_SIZE):
        self.data = [None] * max_size
        self.top = -1
        self.max_size = max_size

    # =======================================================================
    # 관찰자 (Observer) — 값을 바꾸지 않는 연산. 직접 채울 것은 없다.
    # data[0] ~ data[top]만 의미 있는 값이다. data[top]이 맨 위.
    # =======================================================================
    def size(self):
        return self.top + 1

    def isEmpty(self):
        return self.top == -1

    def isFull(self):
        return self.top == self.max_size - 1

    def toList(self):
        """바닥 -> 맨 위 순서로 반환 (확인용)"""
        return [self.data[i] for i in range(self.top + 1)]

    # =======================================================================
    # 문제 1. push / pop / peek — 맨 위(top)에서만 넣고 뺀다 (LIFO)
    #
    #   push(7), push(3), push(6)  ->  data = [7, 3, 6, ...], top = 2
    #   pop()  -> 6 반환             ->  data = [7, 3, ...],    top = 1
    #   ① push: top을 한 칸 올리고 그 자리에 쓴다
    #   ② pop : 맨 위 값을 읽고 top을 한 칸 내린다
    #   ③ peek: 맨 위 값을 읽기만 한다 (top은 그대로)
    # =======================================================================
    def push(self, value):
        if self.isFull():
            raise OverflowError("Stack is full")
        NEED_TO_SOLVE           # 1) top 한 칸 올리기
        NEED_TO_SOLVE           # 2) 그 자리에 value 쓰기

    def pop(self):
        if self.isEmpty():
            raise IndexError("pop from empty stack")
        value = NEED_TO_SOLVE   # 1) 맨 위 값 읽기
        self.data[self.top] = None
        NEED_TO_SOLVE           # 2) top 한 칸 내리기
        return value

    def peek(self):
        if self.isEmpty():
            raise IndexError("peek from empty stack")
        return NEED_TO_SOLVE


# ===========================================================================
# 문제 2. evalPostfix — 후위 표기식 계산기 (문제 1의 ArrayStack을 사용)
#
#   "3 4 + 2 *"  ( = (3 + 4) * 2 )  ->  14
#   토큰을 왼쪽부터 하나씩 읽는다. (토큰은 공백으로 구분되어 있다)
#   ① 숫자면 int로 바꿔 push
#   ② 연산자면 두 개를 pop해서 계산한 뒤 결과를 push
#      먼저 꺼낸 것이 오른쪽(b), 나중에 꺼낸 것이 왼쪽(a) -> a op b
#   ③ 다 읽고 나면 스택에 정확히 1개가 남아야 하고, 그것이 답
#   잘못된 식("1 +", "1 2")은 ValueError를 낸다.
# ===========================================================================
OPERATORS = "+-*/"


def apply(op, a, b):
    """a op b를 계산한다. (주어짐) 나눗셈은 0 쪽으로 버리는 정수 나눗셈 (C와 같음)."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return int(a / b)
    raise ValueError(f"unknown operator: {op}")


def evalPostfix(expr):
    st = ArrayStack()
    for token in expr.split():
        if token in OPERATORS:
            if NEED_TO_SOLVE:       # 꺼낼 피연산자가 2개보다 적으면
                raise ValueError("피연산자가 부족함")
            b = NEED_TO_SOLVE       # 먼저 꺼낸 것 = 오른쪽 피연산자
            a = NEED_TO_SOLVE       # 나중에 꺼낸 것 = 왼쪽 피연산자
            NEED_TO_SOLVE           # apply로 계산한 결과를 다시 push
        else:
            NEED_TO_SOLVE           # 숫자는 int로 바꿔 push

    if NEED_TO_SOLVE:               # 다 읽은 뒤 정확히 1개가 남지 않았으면
        raise ValueError("피연산자가 남음")
    return NEED_TO_SOLVE


# ===========================================================================
# 문제 3. CircularQueue — 원형 큐 (링버퍼)
# ===========================================================================
class CircularQueue:
    """배열(고정 크기)로 구현한 원형 큐.

    front : 맨 앞 원소의 인덱스 (다음에 꺼낼 자리)
    rear  : 다음에 넣을 자리의 인덱스
    한 칸은 항상 비워 둔다 -> 빈 큐(front == rear)와 꽉 찬 큐를 구분하기 위해.
    """

    def __init__(self, capacity=MAX_SIZE):
        self.cap = capacity + 1         # 한 칸은 비워 두므로 +1
        self.data = [None] * self.cap
        self.front = 0
        self.rear = 0

    # =======================================================================
    # 관찰자 (Observer) — 직접 채울 것은 없다. (size는 문제 3에서 채운다)
    # =======================================================================
    def isEmpty(self):
        return self.front == self.rear

    def toList(self):
        """front -> rear 순서로 반환 (확인용)"""
        return [self.data[(self.front + i) % self.cap] for i in range(self.size())]

    def dump(self):
        """배열의 실제 모습과 front/rear 위치 (확인용)"""
        cells = " ".join("." if v is None else str(v) for v in self.data)
        return f"[{cells}]  front={self.front} rear={self.rear}"

    # =======================================================================
    # 문제 3. isFull / size / enqueue / dequeue — 링버퍼
    #
    #   뒤(rear)로 넣고 앞(front)에서 뺀다 (FIFO). 원소를 당기지 않는다.
    #   인덱스가 배열 끝(cap - 1)을 넘으면 0으로 돌아온다 -> % self.cap
    #   ① isFull : rear 다음 칸이 front이면 꽉 찬 것 (한 칸은 비워 두므로)
    #   ② size   : rear - front. 단, rear가 한 바퀴 돌아 front보다 작을 수 있다
    #   ③ enqueue: rear 자리에 쓰고, rear를 한 칸 전진
    #   ④ dequeue: front 자리 값을 읽고, front를 한 칸 전진
    # =======================================================================
    def isFull(self):
        return NEED_TO_SOLVE

    def size(self):
        return NEED_TO_SOLVE

    def enqueue(self, value):
        if self.isFull():
            raise OverflowError("Queue is full")
        self.data[NEED_TO_SOLVE] = value
        self.rear = NEED_TO_SOLVE

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("dequeue from empty queue")
        value = self.data[NEED_TO_SOLVE]
        self.data[self.front] = None
        self.front = NEED_TO_SOLVE
        return value


# ===========================================================================
# 체크포인트 — 구현이 맞는지 확인한다 (수정하지 않아도 됨)
# ===========================================================================
def stack_ops():
    st = ArrayStack(5)
    for v in [7, 3, 6]:
        st.push(v)
    popped = st.pop()
    st.push(4)
    return (popped, st.peek(), st.toList())


def raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


def fill_over(q, values):
    for v in values:
        q.enqueue(v)


def ring_wrap():
    """용량 4짜리 큐에서 넣고 빼기를 반복해 rear가 배열 끝을 넘어가게 만든다."""
    q = CircularQueue(4)
    fill_over(q, [1, 2, 3, 4])
    full = q.isFull()
    a, b = q.dequeue(), q.dequeue()
    q.enqueue(5)
    q.enqueue(6)
    return (full, a, b, q.toList(), q.size(), q.isFull())


def ring_many():
    """용량 3짜리 큐에 1~10을 흘려보낸다. 꽉 차면 하나 꺼내고 넣는다."""
    q = CircularQueue(3)
    out = ArrayStack(20)
    for v in range(1, 11):
        if q.isFull():
            out.push(q.dequeue())
        q.enqueue(v)
    return (out.toList(), q.toList())


CASES = [
    ("문제1 push 7,3,6 -> pop -> push 4", stack_ops,                                              (6, 4, [7, 3, 4])),
    ("문제1 빈 스택 pop -> IndexError",   lambda: raises(lambda: ArrayStack(3).pop(), IndexError),  True),
    ("문제2 '3 4 + 2 *'",                 lambda: evalPostfix("3 4 + 2 *"),                         14),
    ("문제2 '5 1 2 + 4 * + 3 -'",         lambda: evalPostfix("5 1 2 + 4 * + 3 -"),                 14),
    ("문제2 '9 3 /' (순서 주의)",         lambda: evalPostfix("9 3 /"),                             3),
    ("문제2 '2 7 -' (순서 주의)",         lambda: evalPostfix("2 7 -"),                             -5),
    ("문제2 '1 +' -> ValueError",         lambda: raises(lambda: evalPostfix("1 +"), ValueError),   True),
    ("문제2 '1 2' -> ValueError",         lambda: raises(lambda: evalPostfix("1 2"), ValueError),   True),
    ("문제3 넣고 빼며 끝을 넘어가기",     ring_wrap,                                                (True, 1, 2, [3, 4, 5, 6], 4, True)),
    ("문제3 용량 3에 1~10 흘려보내기",    ring_many,                                                ([1, 2, 3, 4, 5, 6, 7], [8, 9, 10])),
    ("문제3 빈 큐 dequeue -> IndexError", lambda: raises(lambda: CircularQueue(2).dequeue(), IndexError), True),
    ("문제3 꽉 찬 큐 enqueue -> OverflowError",
     lambda: raises(lambda: fill_over(CircularQueue(2), [1, 2, 3]), OverflowError),                 True),
]

def run_cases(title, cases):
    print(f"=== {title} ===")
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


def show_ring():
    print("=== 링버퍼 들여다보기 (용량 4 -> 배열 칸은 5개, 한 칸은 항상 비움) ===")
    q = CircularQueue(4)
    steps = [("enqueue", 1), ("enqueue", 2), ("enqueue", 3), ("enqueue", 4),
             ("dequeue", None), ("dequeue", None), ("enqueue", 5), ("enqueue", 6)]
    for op, v in steps:
        if op == "enqueue":
            q.enqueue(v)
            label = f"enqueue({v})"
        else:
            label = f"dequeue() -> {q.dequeue()}"
        print(f"  {label:<14} {q.dump()}")
    print()


# ===========================================================================
# 문제 4. 당겨서 빼는 큐 vs 원형 큐 비교 실험 (코드는 주어진다. 결과를 읽고 해석한다)
#
#  - ShiftQueue: 늘 data[0]에서 꺼내고, 남은 원소를 전부 한 칸씩 앞으로 당긴다
#  - CircularQueue: front만 한 칸 전진한다 (문제 3)
#  - 볼 것: 원소 수 N이 2배가 될 때 dequeue 한 번의 비용이 어떻게 변하는가
# ===========================================================================
class ShiftQueue:
    """배열 맨 앞에서 꺼내고, 나머지를 한 칸씩 앞으로 당기는 큐 (비교용)."""

    def __init__(self, capacity=MAX_SIZE):
        self.data = [None] * capacity
        self.length = 0
        self.cap = capacity

    def enqueue(self, value):
        if self.length == self.cap:
            raise OverflowError("Queue is full")
        self.data[self.length] = value
        self.length += 1

    def dequeue(self):
        if self.length == 0:
            raise IndexError("dequeue from empty queue")
        value = self.data[0]
        i = 0
        while i < self.length - 1:      # 뒤 원소를 전부 한 칸씩 당김 -> O(N)
            self.data[i] = self.data[i + 1]
            i += 1
        self.length -= 1
        self.data[self.length] = None
        return value


def measure(make, n, repeat):
    """원소 n개가 들어 있는 큐에서 dequeue + enqueue 1회에 걸린 평균 시간(us)."""
    q = make(n + 1)
    for i in range(n):
        q.enqueue(i)
    start = time.perf_counter()
    for _ in range(repeat):
        q.enqueue(q.dequeue())
    return (time.perf_counter() - start) / repeat * 1_000_000


def run_experiment():
    print("=== 문제 4. dequeue + enqueue 1회 — ShiftQueue(당기기) vs CircularQueue(링버퍼) ===")
    print("       N |  ShiftQueue | CircularQueue")
    print("-" * 40)
    for n in (1000, 2000, 4000, 8000, 16000):
        shift_us = measure(ShiftQueue, n, 100)
        ring_us = measure(CircularQueue, n, 5000)
        print(f"{n:>8} | {shift_us:>9.1f}us | {ring_us:>11.3f}us")
    print("N이 2배가 되면 ShiftQueue도 약 2배 -> O(N)")
    print("CircularQueue는 N이 커져도 그대로 -> O(1)\n")

    print("생각해보기")
    print("  1. 링버퍼에서 한 칸을 비워 두지 않으면 빈 큐와 꽉 찬 큐를 어떻게 구분할 수 있는가?")
    print("  2. ShiftQueue 대신 '앞에서 빼고 front만 증가'시키면 어떤 문제가 생기는가? (원형이 아닐 때)")


if __name__ == "__main__":
    if run_cases("체크포인트", CASES):
        show_ring()
        run_experiment()
    else:
        print("체크포인트를 먼저 통과시킨 뒤 실험을 돌린다.")
