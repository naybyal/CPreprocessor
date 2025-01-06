// Converted macro: #define _SSP_STDIO_H 1
extern char *__gets_chk (char *__str, size_t);
extern int __snprintf_chk (char *__restrict__ __s, size_t __n, int __flag,
extern int __sprintf_chk (char *__restrict__ __s, int __flag, size_t __slen,
extern int __vsnprintf_chk (char *__restrict__ __s, size_t __n, int __flag,
extern int __vsprintf_chk (char *__restrict__ __s, int __flag, size_t __slen,
fgets (char *__restrict__ __s, int __n, FILE *__restrict__ __stream)
int getPriority(char x) {
gets (char *__str)
int isOperator(char x) {
int main() {
char pop() {
void push(char x) {
// Converted macro: #define snprintf(str, len, ...) \
// Converted macro: #define sprintf(str, ...) \
char stack[100];
int top = -1;
// Converted macro: #define vsnprintf(str, len, fmt, ap) \
// Converted macro: #define vsprintf(str, fmt, ap) \
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


    switch (x) {
        case '(':
        case ')':
        case '^':
        case '%':
        case '/':
        case '*':
        case '+':
        case '-':
        case '=':
            return 1;
        default:
            return 0;
    }
}

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
