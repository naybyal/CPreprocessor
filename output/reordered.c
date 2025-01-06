#define _SSP_STDIO_H 1
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
#define snprintf(str, len, ...) \
#define sprintf(str, ...) \
char stack[100];
int top = -1;
#define vsnprintf(str, len, fmt, ap) \
#define vsprintf(str, fmt, ap) \
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
        default:    
            return 11;
    }
}

    stack[++top] = x;
}

    if (top >= 0)
        return stack[top--];
    else
        return '$';
}

    int i, length, k = 0;
    char inputString[100], postfixForm[100], x, first, second, temp;
    push('$');

    printf("Enter the expression\t->\t");
    scanf("%s", inputString);
    length = strlen(inputString);
    for (i=0; i<length; i++) {
        if (inputString[i] == '-' && (i == 0 || isOperator(inputString[i-1])))
            inputString[i] = '_';
    }
    for (i=0; i<length; i++) {

        if (isOperator(inputString[i])) {

            if (top <= 0 || stack[top] == '(' || inputString[i] == '(') 
                push(inputString[i]);
            else if (inputString[i] == ')') 
                while ((x = pop()) != '(') 
                    postfixForm[k++] = x;
            else if (inputString[i] == '_')
                postfixForm[k++] = inputString[i];
            else if (getPriority(inputString[i]) < getPriority(stack[top--]))
                push(inputString[i]);
            else {
                postfixForm[k++] = pop();
                push(inputString[i]);
            }

        } else postfixForm[k++] = inputString[i];
        
    }

    while ((x = pop()) != '$')
        postfixForm[k++] = x;
    postfixForm[k++] = '\0'; 

    printf("Postfix : %s", postfixForm);
    printf("\nOperator\tArg1\tArg2 (Result)\n");
    for (i=0; postfixForm[i] != '\0'; i++) {
        if (!isOperator(postfixForm[i]))
            push(postfixForm[i]);
        else {
            if (postfixForm[i] == '_' || postfixForm[i] == '=')
                second = '_';
            else    second = pop();

            first = pop();

            if (postfixForm[i] == '_') {
                printf("%s\t%c\t%c\n", "Uminus", first, second);
                push(second);
            } else {
                if (postfixForm[i] == '=') {
                    temp = pop();
                    printf("%c\t\t%c\t%c\n", postfixForm[i], first, temp);
                } else {
                    printf("%c\t\t%c\t%c\n", postfixForm[i], first, second);
                    push(second);
                }
            }
        }
    }
}
#ifndef _SSP_STDIO_H

#include <ssp.h>
#include_next <stdio.h>

#if __SSP_FORTIFY_LEVEL > 0

#include <stdarg.h>

#undef sprintf
#undef vsprintf
#undef snprintf
#undef vsnprintf
#undef gets
#undef fgets

			  __const char *__restrict__ __format, ...);
			   __const char *__restrict__ __format,
			   va_list __ap);

  __builtin___sprintf_chk (str, 0, __ssp_bos (str), \
			   __VA_ARGS__)
  __builtin___vsprintf_chk (str, 0, __ssp_bos (str), fmt, ap)

			   size_t __slen, __const char *__restrict__ __format,
			   ...);
			    size_t __slen, __const char *__restrict__ __format,
			    va_list __ap);

  __builtin___snprintf_chk (str, len, 0, __ssp_bos (str), __VA_ARGS__)
  __builtin___vsnprintf_chk (str, len, 0, __ssp_bos (str), fmt, ap)

extern char *__SSP_REDIRECT (__gets_alias, (char *__str), gets);

extern inline __attribute__((__always_inline__)) char *
{
  if (__ssp_bos (__str) != (size_t) -1)
    return __gets_chk (__str, __ssp_bos (__str));
  return __gets_alias (__str);
}

extern char *__SSP_REDIRECT (__fgets_alias,
			     (char *__restrict__ __s, int __n,
			      FILE *__restrict__ __stream), fgets);

extern inline __attribute__((__always_inline__)) char *
{
  if (__ssp_bos (__s) != (size_t) -1 && (size_t) __n > __ssp_bos (__s))
    __chk_fail ();
  return __fgets_alias (__s, __n, __stream);
}

#endif /* __SSP_FORTIFY_LEVEL > 0 */
#endif /* _SSP_STDIO_H */
