// practice.cpp — 10주차 실습: Floyd 사이클 탐지 / 이중 연결 리스트 위치별 삽입·삭제
//
// 구현된 함수 6개를 슬라이드와 같이 읽고, 실행 결과를 확인한다.
//   1부: floyd_meet, cycle_start
//   2부: dl_pop_front, dl_pop_back, dl_insert_at, dl_erase_at
// 크래시 예시: crash_demo.cpp (floyd_meet의 while 조건을 잘못 쓴 버전)
//
// 빌드: g++ -Wall -o practice practice.cpp && ./practice
// 메모리 검사: g++ -Wall -g -fsanitize=address -o practice practice.cpp && ./practice

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <new>

#ifndef _WIN32
#include <signal.h>
#include <sys/wait.h>
#include <unistd.h>
#endif

using namespace std;

// ===========================================================================
// new / delete 호출 횟수를 세는 장치 (수정하지 않아도 됨)
// alloc_count = 아직 delete하지 않은 블록 개수. 다 지운 뒤 0이어야 한다.
// ===========================================================================
static int alloc_count = 0;

void *operator new(size_t size) {
    void *p = malloc(size);
    if (p == nullptr) throw bad_alloc();
    alloc_count++;
    return p;
}

void operator delete(void *p) noexcept {
    if (p == nullptr) return;
    alloc_count--;
    free(p);
}

void operator delete(void *p, size_t) noexcept { operator delete(p); }

#define BUF 512   // 체크포인트 결과 문자열 크기
#define MAXN 32   // 테스트에서 만드는 노드 최대 개수

// ===========================================================================
// 1부. 단일 연결 리스트의 사이클
//
//   정상:   head -> [1] -> [2] -> [3] -> [4] -> nullptr
//   사이클: head -> [1] -> [2] -> [3] -> [4]
//                          ^             |
//                          +-------------+   (4의 next가 2를 가리킴)
//
//   사이클이 있으면 nullptr이 나오지 않는다 -> cur != nullptr 순회가 끝나지 않는다.
// ===========================================================================
struct Node {
    int data;
    Node *next;
};

// 노드 n개를 만들어 1, 2, ..., n 순서로 잇는다. nodes[i] = i번째 노드 (테스트 정리용)
// (수정하지 않아도 됨)
static Node *build_list(int n, Node *nodes[]) {
    Node *head = nullptr;
    for (int i = n - 1; i >= 0; i--) {
        Node *node = new Node;
        node->data = i + 1;
        node->next = head;
        head = node;
        nodes[i] = node;
    }
    return head;
}

// 마지막 노드의 next를 k번째 노드(0부터)로 바꿔 사이클을 만든다. k < 0이면 그대로.
static void make_cycle(Node *nodes[], int n, int k) {
    if (n == 0 || k < 0) return;
    nodes[n - 1]->next = nodes[k];
}

// 노드 주소를 nodes 배열로 기억해 두었다가 직접 delete (사이클이 있어도 안전)
static void free_nodes(Node *nodes[], int n) {
    for (int i = 0; i < n; i++) delete nodes[i];
}

// ===========================================================================
// 0단계. 웜업 — 사이클이 있는 리스트를 순회하면 (직접 채울 것 없음)
//   최대 limit개까지만 출력하도록 막아 두었다.
// ===========================================================================
static void print_limited(Node *head, int limit) {
    int count = 0;
    for (Node *cur = head; cur != nullptr; cur = cur->next) {
        if (count == limit) { printf("... (%d개 넘음, 끝나지 않음)", limit); break; }
        printf("%d ", cur->data);
        count++;
    }
    printf("\n");
}

void warmup() {
    Node *nodes[MAXN];
    Node *head = build_list(5, nodes);
    printf("사이클 없음 : ");
    print_limited(head, 15);

    make_cycle(nodes, 5, 2);          // 5의 next -> 3
    printf("5 -> 3 연결 : ");
    print_limited(head, 15);
    free_nodes(nodes, 5);
}

// ===========================================================================
// 함수 1. floyd_meet — 두 포인터가 만나는 노드 찾기
//
//   slow: 1칸씩 (slow = slow->next)
//   fast: 2칸씩 (fast = fast->next->next)
//   - 사이클 없음: fast가 먼저 끝(nullptr)에 도착 -> nullptr 반환
//   - 사이클 있음: 둘 다 사이클 안에서 돌고, 한 번에 거리가 1씩 줄어 언젠가 만난다
//                  -> 만난 노드 반환
//
//   while 조건: fast->next->next를 읽으려면 fast와 fast->next 둘 다 nullptr이 아니어야 한다
//
//   has_cycle은 floyd_meet의 결과만 본다 (주어짐)
// ===========================================================================
Node *floyd_meet(Node *head) {
    Node *slow = head;
    Node *fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;            // ① slow 1칸 이동
        fast = fast->next->next;      // ② fast 2칸 이동
        if (slow == fast) {
            return slow;              // ③ 만났으면 그 노드 반환
        }
    }
    return nullptr;                   // fast가 끝에 도착 -> 사이클 없음
}

int has_cycle(Node *head) {
    return floyd_meet(head) != nullptr;
}

// ===========================================================================
// 함수 2. cycle_start — 사이클이 시작되는 노드
//
//   a = head에서 사이클 시작까지 거리, c = 사이클 길이
//   만날 때까지 slow가 간 거리 = s, fast가 간 거리 = 2s
//   fast는 slow보다 사이클을 몇 바퀴 더 돈 것 -> 2s - s = s 는 c의 배수
//   -> meet에서 a칸 더 가면 사이클 시작에 도착 (슬라이드 참고)
//
//   ① p = head, q = meet
//   ② 둘 다 1칸씩 이동, 만나는 노드 = 사이클 시작
//   사이클이 없으면 nullptr
// ===========================================================================
Node *cycle_start(Node *head) {
    Node *meet = floyd_meet(head);
    if (meet == nullptr) return nullptr;

    Node *p = head;
    Node *q = meet;
    while (p != q) {
        p = p->next;                  // ② p 1칸
        q = q->next;                  // ② q 1칸
    }
    return p;
}

// ===========================================================================
// 2부. 이중 연결 리스트 — 맨 앞 / 맨 뒤 / 중간(위치 pos) 삽입·삭제
//
//   head -> [nullptr|1|next] <-> [back|2|next] <-> [back|3|nullptr] <- tail
//   위치(pos)는 0부터. pos = 0 이 첫 노드, pos = size - 1 이 마지막 노드
// ===========================================================================
struct DNode {
    int data;
    DNode *back;
    DNode *next;
};

struct DList {
    DNode *head;
    DNode *tail;
    int size;
};

void dl_init(DList *list) {
    list->head = nullptr;
    list->tail = nullptr;
    list->size = 0;
}

// 9주차에 만든 함수 (주어짐)
DNode *create_dnode(int data) {
    DNode *node = new DNode;
    node->data = data;
    node->back = nullptr;
    node->next = nullptr;
    return node;
}

void dl_push_front(DList *list, int data) {
    DNode *node = create_dnode(data);
    node->next = list->head;
    if (list->head == nullptr) list->tail = node;
    else list->head->back = node;
    list->head = node;
    list->size++;
}

void dl_push_back(DList *list, int data) {
    DNode *node = create_dnode(data);
    node->back = list->tail;
    if (list->tail == nullptr) list->head = node;
    else list->tail->next = node;
    list->tail = node;
    list->size++;
}

void dl_clear(DList *list) {
    DNode *cur = list->head;
    while (cur != nullptr) {
        DNode *next = cur->next;
        delete cur;
        cur = next;
    }
    dl_init(list);
}

// ===========================================================================
// 함수 3. dl_pop_front — 맨 앞 삭제, O(1)
//
//   전: head -> [1] <-> [2] <-> [3]
//   후: head -> [2] <-> [3]          (2의 back = nullptr)
//   ① head = 첫 노드의 next
//   ② 리스트가 비었으면 tail = nullptr, 아니면 새 첫 노드의 back = nullptr
//   ③ delete
//   삭제한 값은 *out에 저장. 성공 1, 빈 리스트면 0
// ===========================================================================
int dl_pop_front(DList *list, int *out) {
    if (list->head == nullptr) return 0;
    DNode *node = list->head;
    *out = node->data;

    list->head = node->next;          // ①
    if (list->head == nullptr) {      // ② 원소가 1개였음
        list->tail = nullptr;         // ②
    } else {
        list->head->back = nullptr;   // ②
    }
    delete node;                      // ③
    list->size--;
    return 1;
}

// ===========================================================================
// 함수 4. dl_pop_back — 맨 뒤 삭제, O(1)
//
//   dl_pop_front와 대칭 (head <-> tail, next <-> back)
//   단일 연결 리스트는 맨 뒤 삭제가 O(N) (마지막 앞 노드를 찾으러 head부터 이동)
//   이중 연결 리스트는 tail->back으로 바로 간다
// ===========================================================================
int dl_pop_back(DList *list, int *out) {
    if (list->tail == nullptr) return 0;
    DNode *node = list->tail;
    *out = node->data;

    list->tail = node->back;          // ①
    if (list->tail == nullptr) {      // ② 원소가 1개였음
        list->head = nullptr;         // ②
    } else {
        list->tail->next = nullptr;   // ②
    }
    delete node;                      // ③
    list->size--;
    return 1;
}

// ===========================================================================
// 보조 함수. dl_node_at — pos번째 노드 찾기 (주어짐)
//
//   pos가 앞쪽 절반이면 head에서 next로 pos번 이동
//   뒤쪽 절반이면 tail에서 back으로 (size - 1 - pos)번 이동
//   -> 최대 이동 횟수가 size / 2 로 준다
//   범위 밖이면 nullptr
// ===========================================================================
DNode *dl_node_at(DList *list, int pos) {
    if (pos < 0 || pos >= list->size) return nullptr;

    DNode *cur;
    if (pos < list->size / 2) {
        cur = list->head;
        for (int i = 0; i < pos; i++) {
            cur = cur->next;          // head에서 앞으로
        }
    } else {
        cur = list->tail;
        for (int i = list->size - 1; i > pos; i--) {
            cur = cur->back;          // tail에서 뒤로
        }
    }
    return cur;
}

// ===========================================================================
// 함수 5. dl_insert_at — pos 위치에 삽입 (새 노드가 pos번째가 된다)
//
//   pos == 0    -> dl_push_front,  pos == size -> dl_push_back  (주어짐)
//   중간: cur = pos번째 노드, prev = cur->back. 새 노드는 prev와 cur 사이에 들어간다
//
//     전: [prev] <-> [cur]
//     후: [prev] <-> [node] <-> [cur]
//
//   ① 새 노드의 포인터 2개: node->back = prev, node->next = cur
//   ② 이웃의 포인터 2개:   prev->next = node, cur->back = node
//   성공 1, pos가 범위 밖이면 0
// ===========================================================================
int dl_insert_at(DList *list, int pos, int data) {
    if (pos < 0 || pos > list->size) return 0;
    if (pos == 0)          { dl_push_front(list, data); return 1; }
    if (pos == list->size) { dl_push_back(list, data);  return 1; }

    DNode *cur = dl_node_at(list, pos);
    DNode *prev = cur->back;
    DNode *node = create_dnode(data);

    node->back = prev;                // ①
    node->next = cur;                 // ①
    prev->next = node;                // ②
    cur->back = node;                 // ②
    list->size++;
    return 1;
}

// ===========================================================================
// 함수 6. dl_erase_at — pos번째 노드 삭제
//
//   pos == 0 -> dl_pop_front,  pos == size - 1 -> dl_pop_back  (주어짐)
//   중간: cur의 앞 노드와 뒤 노드를 서로 잇고 delete
//
//     전: [A] <-> [cur] <-> [B]
//     후: [A] <-> [B]
//
//   ① A->next = B   (A = cur->back, B = cur->next)
//   ② B->back = A
//   ③ delete cur
//   삭제한 값은 *out에 저장. 성공 1, pos가 범위 밖이면 0
// ===========================================================================
int dl_erase_at(DList *list, int pos, int *out) {
    if (pos < 0 || pos >= list->size) return 0;
    if (pos == 0)              return dl_pop_front(list, out);
    if (pos == list->size - 1) return dl_pop_back(list, out);

    DNode *cur = dl_node_at(list, pos);
    *out = cur->data;

    cur->back->next = cur->next;      // ①
    cur->next->back = cur->back;      // ②
    delete cur;                       // ③
    list->size--;
    return 1;
}

// ===========================================================================
// 확인용 출력 함수 (수정하지 않아도 됨)
// ===========================================================================
// head -> tail (next를 따라감). 사이클/끊김이 있어도 멈추도록 최대 MAXN개
static void dl_to_string(DList *list, char *buf) {
    int len = snprintf(buf, BUF, "[");
    int count = 0;
    for (DNode *cur = list->head; cur != nullptr && count < MAXN; cur = cur->next, count++)
        len += snprintf(buf + len, BUF - len, cur == list->head ? "%d" : ", %d", cur->data);
    snprintf(buf + len, BUF - len, "]");
}

// tail -> head (back을 따라감)
static void dl_to_string_backward(DList *list, char *buf) {
    int len = snprintf(buf, BUF, "[");
    int count = 0;
    for (DNode *cur = list->tail; cur != nullptr && count < MAXN; cur = cur->back, count++)
        len += snprintf(buf + len, BUF - len, cur == list->tail ? "%d" : ", %d", cur->data);
    snprintf(buf + len, BUF - len, "]");
}

static void dl_state(DList *list, char *buf) {
    char f[BUF], b[BUF];
    dl_to_string(list, f);
    dl_to_string_backward(list, b);
    snprintf(buf, BUF, "앞->뒤 %s 뒤->앞 %s size=%d", f, b, list->size);
}

static const char *val(Node *n) {
    static char s[16];
    if (n == nullptr) return "nullptr";
    snprintf(s, 16, "%d", n->data);
    return s;
}

// ===========================================================================
// 체크포인트 — 구현이 맞는지 확인한다 (수정하지 않아도 됨)
// ===========================================================================
// n개 리스트, 마지막 노드 -> k번째 노드(k < 0이면 사이클 없음)
static void floyd_case(char *buf, int n, int k) {
    alloc_count = 0;
    Node *nodes[MAXN];
    Node *head = build_list(n, nodes);
    make_cycle(nodes, n, k);
    int has = has_cycle(head);
    char start[16];
    snprintf(start, 16, "%s", val(cycle_start(head)));   // delete 전에 값 읽기
    free_nodes(nodes, n);
    snprintf(buf, BUF, "has=%d start=%s alloc=%d", has, start, alloc_count);
}

static void case_f_empty(char *buf)  { floyd_case(buf, 0, -1); }
static void case_f_one(char *buf)    { floyd_case(buf, 1, -1); }
static void case_f_even(char *buf)   { floyd_case(buf, 6, -1); }
static void case_f_odd(char *buf)    { floyd_case(buf, 7, -1); }
static void case_f_self(char *buf)   { floyd_case(buf, 1, 0); }
static void case_f_ring(char *buf)   { floyd_case(buf, 5, 0); }
static void case_f_mid(char *buf)    { floyd_case(buf, 8, 3); }
static void case_f_tail(char *buf)   { floyd_case(buf, 10, 9); }

static void case_pop_front(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    for (int i = 1; i <= 3; i++) dl_push_back(&l, i);
    int a = 0;
    int r1 = dl_pop_front(&l, &a);
    char s[BUF]; dl_state(&l, s);
    snprintf(buf, BUF, "pop=%d(%d) %s alloc=%d", a, r1, s, alloc_count);
    dl_clear(&l);
}

static void case_pop_front_all(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    dl_push_back(&l, 1); dl_push_back(&l, 2);
    int a = 0, b = 0, c = 0;
    int r = dl_pop_front(&l, &a) + dl_pop_front(&l, &b) + dl_pop_front(&l, &c);
    snprintf(buf, BUF, "값 %d,%d ret합=%d head=%s tail=%s alloc=%d", a, b, r,
             l.head == nullptr ? "nullptr" : "?", l.tail == nullptr ? "nullptr" : "?", alloc_count);
}

static void case_pop_back(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    for (int i = 1; i <= 3; i++) dl_push_back(&l, i);
    int a = 0;
    int r1 = dl_pop_back(&l, &a);
    char s[BUF]; dl_state(&l, s);
    snprintf(buf, BUF, "pop=%d(%d) %s alloc=%d", a, r1, s, alloc_count);
    dl_clear(&l);
}

static void case_pop_back_all(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    dl_push_back(&l, 1); dl_push_back(&l, 2);
    int a = 0, b = 0, c = 0;
    int r = dl_pop_back(&l, &a) + dl_pop_back(&l, &b) + dl_pop_back(&l, &c);
    snprintf(buf, BUF, "값 %d,%d ret합=%d head=%s tail=%s alloc=%d", a, b, r,
             l.head == nullptr ? "nullptr" : "?", l.tail == nullptr ? "nullptr" : "?", alloc_count);
}

static void case_insert_at(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    int r = 0;
    r += dl_insert_at(&l, 0, 20);   // [20]
    r += dl_insert_at(&l, 0, 10);   // [10, 20]          맨 앞
    r += dl_insert_at(&l, 2, 40);   // [10, 20, 40]      맨 뒤
    r += dl_insert_at(&l, 2, 30);   // [10, 20, 30, 40]  중간
    r += dl_insert_at(&l, 1, 15);   // [10, 15, 20, 30, 40]
    r += dl_insert_at(&l, 9, 99);   // 범위 밖 -> 0
    char s[BUF]; dl_state(&l, s);
    snprintf(buf, BUF, "%s ret합=%d alloc=%d", s, r, alloc_count);
    dl_clear(&l);
}

static void case_erase_at(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    for (int i = 1; i <= 6; i++) dl_push_back(&l, i);   // [1..6]
    int a = 0, b = 0, c = 0, d = 0, e = 0;
    int r = dl_erase_at(&l, 2, &a)    // 중간: 3 -> [1, 2, 4, 5, 6]
          + dl_erase_at(&l, 0, &b)    // 맨 앞: 1 -> [2, 4, 5, 6]
          + dl_erase_at(&l, 3, &c)    // 맨 뒤: 6 -> [2, 4, 5]
          + dl_erase_at(&l, 1, &d)    // 중간: 4 -> [2, 5]
          + dl_erase_at(&l, 5, &e);   // 범위 밖 -> 0
    char s[BUF]; dl_state(&l, s);
    snprintf(buf, BUF, "삭제 %d,%d,%d,%d %s ret합=%d alloc=%d", a, b, c, d, s, r, alloc_count);
    dl_clear(&l);
}

static void case_mixed(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    int x;
    for (int i = 1; i <= 5; i++) dl_insert_at(&l, l.size / 2, i);   // 항상 가운데에 삽입
    char s1[BUF]; dl_state(&l, s1);
    while (l.size > 0) dl_erase_at(&l, l.size / 2, &x);             // 항상 가운데를 삭제
    snprintf(buf, BUF, "%s / 전부 삭제 후 head=%s tail=%s alloc=%d", s1,
             l.head == nullptr ? "nullptr" : "?", l.tail == nullptr ? "nullptr" : "?", alloc_count);
}

struct Case {
    const char *name;
    void (*fn)(char *buf);
    const char *expected;
};

static Case CASES[] = {
    {"함수1,2 빈 리스트",                  case_f_empty,  "has=0 start=nullptr alloc=0"},
    {"함수1,2 노드 1개, 사이클 없음",      case_f_one,    "has=0 start=nullptr alloc=0"},
    {"함수1,2 노드 6개, 사이클 없음",      case_f_even,   "has=0 start=nullptr alloc=0"},
    {"함수1,2 노드 7개, 사이클 없음",      case_f_odd,    "has=0 start=nullptr alloc=0"},
    {"함수1,2 노드 1개, 자기 자신",        case_f_self,   "has=1 start=1 alloc=0"},
    {"함수1,2 5개, 5 -> 1 (전체가 원)",    case_f_ring,   "has=1 start=1 alloc=0"},
    {"함수1,2 8개, 8 -> 4",                case_f_mid,    "has=1 start=4 alloc=0"},
    {"함수1,2 10개, 10 -> 10",             case_f_tail,   "has=1 start=10 alloc=0"},
    {"함수3 [1, 2, 3]에서 pop_front",      case_pop_front,     "pop=1(1) 앞->뒤 [2, 3] 뒤->앞 [3, 2] size=2 alloc=2"},
    {"함수3 [1, 2]에서 pop_front 3번",     case_pop_front_all, "값 1,2 ret합=2 head=nullptr tail=nullptr alloc=0"},
    {"함수4 [1, 2, 3]에서 pop_back",       case_pop_back,      "pop=3(1) 앞->뒤 [1, 2] 뒤->앞 [2, 1] size=2 alloc=2"},
    {"함수4 [1, 2]에서 pop_back 3번",      case_pop_back_all,  "값 2,1 ret합=2 head=nullptr tail=nullptr alloc=0"},
    {"함수5 insert_at 앞/뒤/중간/범위 밖", case_insert_at,     "앞->뒤 [10, 15, 20, 30, 40] 뒤->앞 [40, 30, 20, 15, 10] size=5 ret합=5 alloc=5"},
    {"함수6 erase_at 중간/앞/뒤/범위 밖",  case_erase_at,      "삭제 3,1,6,4 앞->뒤 [2, 5] 뒤->앞 [5, 2] size=2 ret합=4 alloc=2"},
    {"함수5+6 가운데 삽입 5번, 가운데 삭제", case_mixed,       "앞->뒤 [2, 4, 5, 3, 1] 뒤->앞 [1, 3, 5, 4, 2] size=5 / 전부 삭제 후 head=nullptr tail=nullptr alloc=0"},
};

// 케이스 하나 실행. 통과하면 1.
// 리눅스/맥: 자식 프로세스에서 실행 -> nullptr 역참조로 죽거나 무한 루프여도 다음 케이스로 넘어감
static int run_one(const Case *c) {
    char buf[BUF] = "";
#ifndef _WIN32
    fflush(stdout);
    pid_t pid = fork();
    if (pid == 0) {
        alarm(2);
        c->fn(buf);
        int passed = strcmp(buf, c->expected) == 0;
        printf("  [%s] %s: %s", passed ? "PASS" : "FAIL", c->name, buf);
        if (!passed) printf("  (기대: %s)", c->expected);
        printf("\n");
        fflush(stdout);
        _exit(passed ? 0 : 3);
    }
    int status;
    waitpid(pid, &status, 0);
    if (WIFEXITED(status)) {
        if (WEXITSTATUS(status) == 0) return 1;
        if (WEXITSTATUS(status) != 3)
            printf("  [FAIL] %s: 메모리 오류 (위 AddressSanitizer 보고 확인)\n", c->name);
        return 0;
    }
    if (WIFSIGNALED(status) && WTERMSIG(status) == SIGALRM)
        printf("  [FAIL] %s: 2초 초과 (무한 루프 의심)\n", c->name);
    else
        printf("  [FAIL] %s: 비정상 종료 (nullptr 역참조 / 이중 delete 의심)\n", c->name);
    return 0;
#else
    c->fn(buf);
    int passed = strcmp(buf, c->expected) == 0;
    printf("  [%s] %s: %s", passed ? "PASS" : "FAIL", c->name, buf);
    if (!passed) printf("  (기대: %s)", c->expected);
    printf("\n");
    return passed;
#endif
}

static int run_cases() {
    printf("=== 체크포인트 ===\n");
    int ok = 1;
    for (size_t i = 0; i < sizeof(CASES) / sizeof(CASES[0]); i++)
        ok = run_one(&CASES[i]) && ok;
    printf("결과: %s\n\n", ok ? "전부 통과" : "통과하지 못한 항목이 있다");
    return ok;
}

// ===========================================================================
// slow / fast 위치 추적 (코드는 주어진다. 결과를 읽고 해석한다)
//
//   노드 8개, 8 -> 4 사이클 (a = 3, c = 5)
//   - 몇 번째 이동에서 만나는가, 만난 노드는 어디인가
//   - 만난 뒤 p(head에서), q(meet에서)가 몇 번 이동해 어디서 만나는가
// ===========================================================================
static void trace_floyd() {
    printf("=== slow / fast 추적 (8개, 8 -> 4) ===\n");
    Node *nodes[MAXN];
    Node *head = build_list(8, nodes);
    make_cycle(nodes, 8, 3);

    Node *slow = head, *fast = head;
    printf("  이동 | slow | fast\n");
    printf("  %4d | %4d | %4d\n", 0, slow->data, fast->data);
    for (int step = 1; step <= 20; step++) {
        slow = slow->next;
        fast = fast->next->next;
        printf("  %4d | %4d | %4d%s\n", step, slow->data, fast->data, slow == fast ? "  <- 만남" : "");
        if (slow == fast) break;
    }

    Node *p = head, *q = slow;
    int moves = 0;
    printf("  만난 뒤: p는 head(%d)에서, q는 만난 노드(%d)에서 1칸씩\n", p->data, q->data);
    while (p != q) { p = p->next; q = q->next; moves++; }
    printf("  %d번 이동 후 %d에서 만남 = 사이클 시작 (a = %d)\n\n", moves, p->data, moves);
    free_nodes(nodes, 8);

    printf("생각해보기\n");
    printf("  1. 방문한 노드 주소를 전부 저장해 두고 비교해도 사이클을 찾을 수 있다. Floyd 방식과 메모리 사용량을 비교하면?\n");
    printf("  2. fast가 3칸씩 이동해도 사이클이 있으면 반드시 만나는가?\n");
    printf("  3. 사이클의 길이(노드 개수)는 floyd_meet이 돌려준 노드에서 어떻게 셀 수 있는가?\n");
}

int main() {
    printf("=== 0단계: 웜업 ===\n");
    warmup();
    printf("\n");

    if (run_cases()) {
        trace_floyd();
    } else {
        printf("체크포인트를 먼저 통과시킨 뒤 추적을 돌린다.\n");
    }
    return 0;
}
