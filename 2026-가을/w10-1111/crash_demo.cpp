// crash_demo.cpp — 10주차 크래시 예시: floyd_meet의 while 조건을 잘못 쓴 버전
//
// practice.cpp의 floyd_meet과 한 줄만 다르다.
// 노드 4개는 정상, 노드 5개에서 비정상 종료한다.
//
// 빌드: g++ -Wall -o crash_demo crash_demo.cpp && ./crash_demo
// 죽는 줄 찾기: g++ -Wall -g -fsanitize=address -o crash_demo crash_demo.cpp && ./crash_demo

#include <cstdio>

struct Node {
    int data;
    Node *next;
};

// 1, 2, ..., n 리스트 (사이클 없음)
Node *build_list(int n) {
    Node *head = nullptr;
    for (int i = n; i >= 1; i--) {
        Node *node = new Node;
        node->data = i;
        node->next = head;
        head = node;
    }
    return head;
}

void free_list(Node *head) {
    while (head != nullptr) {
        Node *next = head->next;
        delete head;
        head = next;
    }
}

Node *floyd_meet(Node *head) {
    Node *slow = head;
    Node *fast = head;
    while (fast != nullptr) {          // practice.cpp와 다른 줄
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return slow;
    }
    return nullptr;
}

int main() {
    for (int n = 4; n <= 5; n++) {
        Node *head = build_list(n);
        printf("노드 %d개: ", n);
        fflush(stdout);
        Node *meet = floyd_meet(head);
        printf("%s\n", meet == nullptr ? "사이클 없음" : "사이클 있음");
        free_list(head);
    }
    return 0;
}
