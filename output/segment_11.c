        case '-':
        case '=':
            return 1;
        default:
            return 0;
    }
}
int getPriority(char x) {
    switch (x) {
        case '(':
            return 0;
        case '_':
            return 1;
        case '^':
            return 2;
        case '%':
            return 3;
        case '/':
            return 4;
        case '*':
            return 5;
        case '+':
            return 6;
        case '-':
            return 7;
        case ')':
            return 8;
        case '=':
        case '-':
        case '=':
            return 1;
        default:
            return 0;
    }
}
int getPriority(char x) {
    switch (x) {
        case '(':
            return 0;
        case '_':
            return 1;
        case '^':
            return 2;
        case '%':
            return 3;
        case '/':
            return 4;
        case '*':
            return 5;
        case '+':
            return 6;
        case '-':
            return 7;
        case ')':
            return 8;
        case '=':
            return 9;
        case '$':
            return 10;
            return 9;
        case '$':
            return 10;
        default:
            return 11;
    }
}
void push(char x) {
    stack[++top] = x;
