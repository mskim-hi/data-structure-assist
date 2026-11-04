// practice.cpp — 9주차 실습: 포인터로 만드는 단일 / 이중 연결 리스트
//
// 규칙
//  - AI 사용 금지. 직접 채운다.
//  - 노드는 new로 만들고 delete로 반납한다. (배열 사용 금지)
//  - NEED_TO_SOLVE는 아무 동작도 하지 않는 빈 자리다.
//    (컴파일은 되지만, 그대로 두면 결과가 틀린다.)
//
// 빌드: g++ -Wall -o practice practice.cpp && ./practice
// 메모리 검사: g++ -Wall -g -fsanitize=address -o practice practice.cpp && ./practice

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <new>

#ifndef _WIN32
#include <signal.h>
#include <sys/wait.h>
#include <unistd.h>
#endif

using namespace std;

#define NEED_TO_SOLVE /* TODO: 이 부분을 직접 채우세요 */

// ===========================================================================
// new / delete 호출 횟수를 세는 장치 (수정하지 않아도 됨)
// new를 쓰면 alloc_count가 1 늘고, delete를 쓰면 1 준다.
// alloc_count = 아직 delete하지 않은 블록 개수. 리스트를 다 지운 뒤 0이어야 한다.
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

// ===========================================================================
// 0단계. 웜업 — 직접 채울 것은 없다. 실행해서 결과를 확인한다.
//
//   int *p = new int;        : 힙에 int 1개를 만들고, 그 주소를 p에 저장
//   *p = 15;                 : 만든 공간에 값 쓰기
//   delete p; p = nullptr;   : 반납 후 허상 포인터 방지
//
//   노드 3개를 따로 new하면 주소가 연속이라는 보장이 없다.
//   -> 각 노드가 다음 노드의 주소(next)를 들고 있어야 순서대로 따라갈 수 있다.
// ===========================================================================
struct Node {
    int data;
    Node *next;   // 다음 노드의 주소 (없으면 nullptr)
};

void warmup() {
    int *p = new int;
    *p = 15;
    cout << "p = " << p << ", *p = " << *p << endl;
    delete p;
    p = nullptr;

    Node *a = new Node;
    Node *b = new Node;
    Node *c = new Node;
    a->data = 10; a->next = b;
    b->data = 20; b->next = c;
    c->data = 30; c->next = nullptr;

    cout << "a: 주소 " << a << "  data=" << a->data << "  next=" << a->next << endl;
    cout << "b: 주소 " << b << "  data=" << b->data << "  next=" << b->next << endl;
    cout << "c: 주소 " << c << "  data=" << c->data << "  next=" << c->next << endl;

    cout << "a부터 next 따라가기: ";
    for (Node *cur = a; cur != nullptr; cur = cur->next) cout << cur->data << " ";
    cout << endl;

    delete a; delete b; delete c;
    cout << "delete 후 alloc_count = " << alloc_count << endl;
}

// ===========================================================================
// 단일 연결 리스트 (Singly Linked List)
//
//   head -> [10|next] -> [20|next] -> [30|nullptr]
//   head : 첫 노드의 주소 (빈 리스트면 nullptr)
//   size : 노드 개수
// ===========================================================================
struct SList {
    Node *head;
    int size;
};

void sl_init(SList *list) {
    list->head = nullptr;
    list->size = 0;
}

// ===========================================================================
// 문제 1. create_node — 노드 1개를 힙에 만든다
//
//   ① new Node로 힙에 노드 1개를 만든다 (크기는 컴파일러가 계산)
//   ② data를 저장하고, next는 nullptr로 둔다 (new Node는 멤버를 초기화하지 않는다)
// ===========================================================================
Node *create_node(int data) {
    Node *node = nullptr;
    NEED_TO_SOLVE;                  // ① new로 Node 1개를 만들어 node에 저장
    NEED_TO_SOLVE;                  // ② data 저장
    NEED_TO_SOLVE;                  // ② next = nullptr
    return node;
}

// ===========================================================================
// 문제 2. sl_push_front — 맨 앞에 넣기, O(1)
//
//   전: head -> [20] -> [30]
//   후: head -> [10] -> [20] -> [30]
//   ① 새 노드의 next가 지금의 첫 노드를 가리키게 한다
//   ② head가 새 노드를 가리키게 한다
//   (①, ② 순서를 바꾸면 기존 노드들의 주소를 잃는다)
// ===========================================================================
void sl_push_front(SList *list, int data) {
    Node *node = create_node(data);
    if (node == nullptr) return;
    NEED_TO_SOLVE;                  // ① 새 노드의 next = 지금의 첫 노드
    NEED_TO_SOLVE;                  // ② head = 새 노드
    list->size++;
}

// ===========================================================================
// 문제 3. 순회 — sl_find / sl_push_back
//
//   순회 기본형: cur = head에서 시작, cur = cur->next로 이동, cur == nullptr이면 끝
//
//   sl_find     : value가 있는 노드의 주소 반환 (없으면 nullptr)
//   sl_push_back: 마지막 노드(next == nullptr)까지 이동한 뒤 그 뒤에 붙인다, O(N)
//                 빈 리스트면 head가 새 노드
// ===========================================================================
Node *sl_find(SList *list, int value) {
    Node *cur = list->head;
    while (cur != nullptr) {
        NEED_TO_SOLVE;              // 1) cur의 data가 value면 cur 반환
        NEED_TO_SOLVE;              // 2) 다음 노드로 이동
    }
    return nullptr;
}

void sl_push_back(SList *list, int data) {
    Node *node = create_node(data);
    if (node == nullptr) return;

    if (list->head == nullptr) {
        NEED_TO_SOLVE;              // 1) 빈 리스트: head = 새 노드
    } else {
        Node *cur = list->head;
        while (cur->next != nullptr) {
            NEED_TO_SOLVE;          // 2) 다음 노드로 이동
        }
        NEED_TO_SOLVE;              // 3) 마지막 노드 뒤에 연결
    }
    list->size++;
}

// ===========================================================================
// 문제 4. sl_remove / sl_clear — 연결 끊고 delete
//
//   sl_remove(value): value가 있는 첫 노드를 삭제. 삭제하면 1, 없으면 0 반환
//     prev -> [cur] -> next   ==>   prev -> next,  delete cur
//     ① cur를 찾는 동안 바로 앞 노드를 prev에 기억한다
//        (단일 연결 리스트는 뒤로 갈 수 없으므로)
//     ② cur가 첫 노드(prev == nullptr)면 head를, 아니면 prev->next를 cur->next로 바꾼다
//     ③ delete cur
//
//   sl_clear: 모든 노드를 delete
//     delete cur 후에는 cur->next를 읽을 수 없다 (허상 포인터)
//     -> delete 전에 다음 노드 주소를 next에 저장해 둔다
// ===========================================================================
int sl_remove(SList *list, int value) {
    Node *prev = nullptr;
    Node *cur = list->head;

    while (cur != nullptr && cur->data != value) {
        NEED_TO_SOLVE;              // ① prev = 지금 노드
        NEED_TO_SOLVE;              // ① cur = 다음 노드
    }
    if (cur == nullptr) return 0;      // 못 찾음

    if (prev == nullptr) {             // ② 첫 노드 삭제
        NEED_TO_SOLVE;
    } else {
        NEED_TO_SOLVE;
    }
    NEED_TO_SOLVE;                  // ③
    list->size--;
    return 1;
}

void sl_clear(SList *list) {
    Node *cur = list->head;
    while (cur != nullptr) {
        Node *next = nullptr;
        NEED_TO_SOLVE;              // 1) delete 전에 다음 주소 저장
        NEED_TO_SOLVE;              // 2) 지금 노드 반납
        cur = next;                 // 3) 다음 노드로 이동
    }
    list->head = nullptr;
    list->size = 0;
}

// ===========================================================================
// 이중 연결 리스트 (Doubly Linked List)
//
//   head -> [nullptr|10|next] <-> [back|20|next] <-> [back|30|nullptr] <- tail
//   back : 앞 노드의 주소 (첫 노드면 nullptr)
//   next : 뒤 노드의 주소 (마지막 노드면 nullptr)
//   tail : 마지막 노드의 주소 -> 맨 뒤 삽입이 O(1)
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

// ===========================================================================
// 문제 5. create_dnode / dl_push_front / dl_push_back
//
//   create_dnode: create_node와 같고, back도 nullptr로 둔다
//
//   dl_push_front(10):  전 head -> [20] <-> [30]
//                       후 head -> [10] <-> [20] <-> [30]
//     ① node->next = 지금의 첫 노드
//     ② 빈 리스트였으면 tail도 node, 아니면 기존 첫 노드의 back = node
//     ③ head = node
//
//   dl_push_back: dl_push_front와 대칭 (head <-> tail, next <-> back)
// ===========================================================================
DNode *create_dnode(int data) {
    DNode *node = nullptr;
    NEED_TO_SOLVE;                  // new로 DNode 1개
    NEED_TO_SOLVE;                  // data
    NEED_TO_SOLVE;                  // back
    NEED_TO_SOLVE;                  // next
    return node;
}

void dl_push_front(DList *list, int data) {
    DNode *node = create_dnode(data);
    if (node == nullptr) return;

    NEED_TO_SOLVE;                  // ①
    if (list->head == nullptr) {       // ②
        NEED_TO_SOLVE;
    } else {
        NEED_TO_SOLVE;
    }
    NEED_TO_SOLVE;                  // ③
    list->size++;
}

void dl_push_back(DList *list, int data) {
    DNode *node = create_dnode(data);
    if (node == nullptr) return;

    NEED_TO_SOLVE;
    if (list->tail == nullptr) {
        NEED_TO_SOLVE;
    } else {
        NEED_TO_SOLVE;
    }
    NEED_TO_SOLVE;
    list->size++;
}

// ===========================================================================
// 문제 6. dl_remove — 이중 연결 리스트에서 삭제
//
//   [A] <-> [cur] <-> [B]   ==>   [A] <-> [B],  delete cur
//   A = cur->back, B = cur->next
//   cur->back으로 앞 노드에 바로 갈 수 있다 -> prev를 따로 기억할 필요 없음
//   ① 앞쪽: cur가 첫 노드면 head = cur->next, 아니면 A->next = cur->next
//   ② 뒤쪽: cur가 마지막 노드면 tail = cur->back, 아니면 B->back = cur->back
//   ③ delete cur
// ===========================================================================
int dl_remove(DList *list, int value) {
    DNode *cur = list->head;
    while (cur != nullptr && cur->data != value) {
        NEED_TO_SOLVE;              // 다음 노드로 이동
    }
    if (cur == nullptr) return 0;

    if (cur->back == nullptr) {        // ①
        NEED_TO_SOLVE;
    } else {
        NEED_TO_SOLVE;
    }

    if (cur->next == nullptr) {        // ②
        NEED_TO_SOLVE;
    } else {
        NEED_TO_SOLVE;
    }

    NEED_TO_SOLVE;                  // ③
    list->size--;
    return 1;
}

// dl_clear는 주어진다 (sl_clear와 같은 방식)
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
// 확인용 출력 함수 (수정하지 않아도 됨)
// ===========================================================================
static void sl_to_string(SList *list, char *buf) {
    int len = snprintf(buf, BUF, "[");
    for (Node *cur = list->head; cur != nullptr; cur = cur->next)
        len += snprintf(buf + len, BUF - len, cur == list->head ? "%d" : ", %d", cur->data);
    snprintf(buf + len, BUF - len, "] size=%d", list->size);
}

// head -> tail 방향 (next를 따라감)
static void dl_to_string(DList *list, char *buf) {
    int len = snprintf(buf, BUF, "[");
    for (DNode *cur = list->head; cur != nullptr; cur = cur->next)
        len += snprintf(buf + len, BUF - len, cur == list->head ? "%d" : ", %d", cur->data);
    snprintf(buf + len, BUF - len, "]");
}

// tail -> head 방향 (back을 따라감)
static void dl_to_string_backward(DList *list, char *buf) {
    int len = snprintf(buf, BUF, "[");
    for (DNode *cur = list->tail; cur != nullptr; cur = cur->back)
        len += snprintf(buf + len, BUF - len, cur == list->tail ? "%d" : ", %d", cur->data);
    snprintf(buf + len, BUF - len, "]");
}

static void sl_dump(SList *list) {
    printf("  head = %p\n", (void *)list->head);
    for (Node *cur = list->head; cur != nullptr; cur = cur->next)
        printf("  [%p] data=%-3d next=%p\n", (void *)cur, cur->data, (void *)cur->next);
}

// ===========================================================================
// 체크포인트 — 구현이 맞는지 확인한다 (수정하지 않아도 됨)
// 각 함수는 결과를 buf에 문자열로 적는다.
// ===========================================================================
static void case_create_node(char *buf) {
    alloc_count = 0;
    Node *n = create_node(7);
    if (n == nullptr) { snprintf(buf, BUF, "nullptr 반환"); return; }
    snprintf(buf, BUF, "data=%d next=%s alloc=%d", n->data, n->next == nullptr ? "nullptr" : "?", alloc_count);
    delete n;
}

static void case_push_front(char *buf) {
    SList l; sl_init(&l);
    sl_push_front(&l, 1); sl_push_front(&l, 2); sl_push_front(&l, 3);
    sl_to_string(&l, buf);
    sl_clear(&l);
}

static void case_find(char *buf) {
    SList l; sl_init(&l);
    sl_push_front(&l, 30); sl_push_front(&l, 20); sl_push_front(&l, 10);
    Node *a = sl_find(&l, 20);
    Node *b = sl_find(&l, 99);
    snprintf(buf, BUF, "find(20)=%s find(99)=%s",
            a != nullptr && a->data == 20 ? "20" : "?", b == nullptr ? "nullptr" : "?");
    sl_clear(&l);
}

static void case_push_back(char *buf) {
    SList l; sl_init(&l);
    sl_push_back(&l, 2); sl_push_front(&l, 1); sl_push_back(&l, 3); sl_push_back(&l, 4);
    sl_to_string(&l, buf);
    sl_clear(&l);
}

static void case_sl_remove(char *buf) {
    alloc_count = 0;
    SList l; sl_init(&l);
    for (int i = 1; i <= 5; i++) sl_push_back(&l, i);
    int r1 = sl_remove(&l, 3);      // 중간
    int r2 = sl_remove(&l, 1);      // 맨 앞
    int r3 = sl_remove(&l, 5);      // 맨 뒤
    int r4 = sl_remove(&l, 9);      // 없음
    char s[BUF]; sl_to_string(&l, s);
    snprintf(buf, BUF, "%s ret=%d%d%d%d alloc=%d", s, r1, r2, r3, r4, alloc_count);
    sl_clear(&l);
}

static void case_sl_clear(char *buf) {
    alloc_count = 0;
    SList l; sl_init(&l);
    for (int i = 0; i < 5; i++) sl_push_front(&l, i);
    int before = alloc_count;
    sl_clear(&l);
    char s[BUF]; sl_to_string(&l, s);
    snprintf(buf, BUF, "전 alloc=%d / 후 %s alloc=%d", before, s, alloc_count);
}

static void case_dl_push(char *buf) {
    DList l; dl_init(&l);
    dl_push_back(&l, 2); dl_push_front(&l, 1); dl_push_back(&l, 3); dl_push_front(&l, 0);
    char f[BUF], b[BUF];
    dl_to_string(&l, f); dl_to_string_backward(&l, b);
    snprintf(buf, BUF, "앞->뒤 %s 뒤->앞 %s size=%d", f, b, l.size);
    dl_clear(&l);
}

static void case_dl_remove(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    for (int i = 1; i <= 5; i++) dl_push_back(&l, i);
    int r = dl_remove(&l, 3) + dl_remove(&l, 1) + dl_remove(&l, 5) + dl_remove(&l, 9);
    char f[BUF], b[BUF];
    dl_to_string(&l, f); dl_to_string_backward(&l, b);
    snprintf(buf, BUF, "앞->뒤 %s 뒤->앞 %s ret합=%d alloc=%d", f, b, r, alloc_count);
    dl_clear(&l);
}

static void case_dl_remove_all(char *buf) {
    alloc_count = 0;
    DList l; dl_init(&l);
    for (int i = 1; i <= 3; i++) dl_push_back(&l, i);
    int r = dl_remove(&l, 2) + dl_remove(&l, 1) + dl_remove(&l, 3);
    snprintf(buf, BUF, "ret합=%d head=%s tail=%s size=%d alloc=%d",
            r, l.head == nullptr ? "nullptr" : "?", l.tail == nullptr ? "nullptr" : "?", l.size, alloc_count);
}

struct Case {
    const char *name;
    void (*fn)(char *buf);
    const char *expected;
};

static Case CASES[] = {
    {"문제1 create_node(7)",                     case_create_node,   "data=7 next=nullptr alloc=1"},
    {"문제2 push_front 1,2,3",                   case_push_front,    "[3, 2, 1] size=3"},
    {"문제3 find 20 / 99",                       case_find,          "find(20)=20 find(99)=nullptr"},
    {"문제3 back 2, front 1, back 3, back 4",    case_push_back,     "[1, 2, 3, 4] size=4"},
    {"문제4 [1..5]에서 3,1,5,9 삭제",            case_sl_remove,     "[2, 4] size=2 ret=1110 alloc=2"},
    {"문제4 sl_clear 후 남은 블록",              case_sl_clear,      "전 alloc=5 / 후 [] size=0 alloc=0"},
    {"문제5 back 2, front 1, back 3, front 0",   case_dl_push,       "앞->뒤 [0, 1, 2, 3] 뒤->앞 [3, 2, 1, 0] size=4"},
    {"문제6 [1..5]에서 3,1,5,9 삭제",            case_dl_remove,     "앞->뒤 [2, 4] 뒤->앞 [4, 2] ret합=3 alloc=2"},
    {"문제6 전부 삭제하면 head/tail 모두 nullptr",  case_dl_remove_all, "ret합=3 head=nullptr tail=nullptr size=0 alloc=0"},
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
        _exit(passed ? 0 : 1);
    }
    int status;
    waitpid(pid, &status, 0);
    if (WIFEXITED(status)) return WEXITSTATUS(status) == 0;
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

static void show_slist() {
    printf("=== 단일 연결 리스트 들여다보기 (push_back 10, 20, 30) ===\n");
    SList l; sl_init(&l);
    sl_push_back(&l, 10); sl_push_back(&l, 20); sl_push_back(&l, 30);
    sl_dump(&l);
    printf("  -> 각 노드의 next = 다음 노드의 주소. 주소가 연속일 필요는 없다.\n\n");
    sl_clear(&l);
}

// ===========================================================================
// 문제 7. 맨 뒤 삽입 비교 실험 (코드는 주어진다. 결과를 읽고 해석한다)
//
//  - SList: sl_push_back이 head부터 끝까지 이동 -> O(N)
//  - DList: tail로 바로 접근 -> O(1)
//  - 볼 것: 원소 수 N이 2배가 될 때 push_back 1회 비용이 어떻게 변하는가
// ===========================================================================
static double us_since(clock_t start) {
    return (double)(clock() - start) * 1000000.0 / CLOCKS_PER_SEC;
}

static void run_experiment() {
    const int ADD = 1000;
    printf("=== 문제 7. 원소 N개가 있을 때 push_back 1회 — SList vs DList ===\n");
    printf("       N |    SList |   DList\n");
    printf("----------------------------------\n");
    for (int n = 4000; n <= 64000; n *= 2) {
        SList s; sl_init(&s);
        DList d; dl_init(&d);
        for (int i = 0; i < n; i++) { sl_push_front(&s, i); dl_push_front(&d, i); }

        clock_t t0 = clock();
        for (int i = 0; i < ADD; i++) sl_push_back(&s, i);
        double s_us = us_since(t0) / ADD;

        clock_t t1 = clock();
        for (int i = 0; i < ADD * 100; i++) dl_push_back(&d, i);
        double d_us = us_since(t1) / (ADD * 100);

        printf("%8d | %6.2fus | %6.3fus\n", n, s_us, d_us);
        sl_clear(&s);
        dl_clear(&d);
    }
    printf("N이 2배가 되면 SList도 약 2배 -> O(N)\n");
    printf("DList는 N이 커져도 그대로 -> O(1)\n");
    printf("실험 후 alloc_count = %d (0이면 누수 없음)\n\n", alloc_count);

    printf("생각해보기\n");
    printf("  1. sl_push_front의 ①, ② 순서를 바꾸면 리스트가 어떻게 되는가?\n");
    printf("  2. void push_front(Node *head, int data)처럼 head를 값으로 받으면 왜 리스트가 안 바뀌는가? (swap1과 비교)\n");
    printf("  3. SList에 tail 포인터만 추가하면 push_back은 O(1)이 된다. 맨 뒤 삭제도 O(1)이 되는가?\n");
}

int main() {
    printf("=== 0단계: 웜업 ===\n");
    warmup();
    printf("\n");

    if (run_cases()) {
        show_slist();
        run_experiment();
    } else {
        printf("체크포인트를 먼저 통과시킨 뒤 실험을 돌린다.\n");
    }
    return 0;
}
