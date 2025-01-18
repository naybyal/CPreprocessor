# 861 "/usr/include/stdlib.h" 3 4
extern int abs (int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern long int labs (long int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
__extension__ extern long long int llabs (long long int __x)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern long int labs (long int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern long int labs (long int __x) __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
__extension__ extern long long int llabs (long long int __x)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern div_t div (int __numer, int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern ldiv_t ldiv (long int __numer, long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
extern ldiv_t ldiv (long int __numer, long int __denom)
extern ldiv_t ldiv (long int __numer, long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
__extension__ extern lldiv_t lldiv (long long int __numer,
__extension__ extern lldiv_t lldiv (long long int __numer,
__extension__ extern lldiv_t lldiv (long long int __numer,
__extension__ extern lldiv_t lldiv (long long int __numer,
        long long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
# 943 "/usr/include/stdlib.h" 3 4
        long long int __denom)
        long long int __denom)
        long long int __denom)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__const__)) ;
# 943 "/usr/include/stdlib.h" 3 4
extern int mblen (const char *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int mbtowc (wchar_t *__restrict __pwc,
     const char *__restrict __s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int wctomb (char *__s, wchar_t __wchar) __attribute__ ((__nothrow__ , __leaf__));
extern size_t mbstowcs (wchar_t *__restrict __pwcs,
extern int mblen (const char *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int mblen (const char *__s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int mbtowc (wchar_t *__restrict __pwc,
extern int mbtowc (wchar_t *__restrict __pwc,
extern int mbtowc (wchar_t *__restrict __pwc,
extern int mbtowc (wchar_t *__restrict __pwc,
     const char *__restrict __s, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
extern int wctomb (char *__s, wchar_t __wchar) __attribute__ ((__nothrow__ , __leaf__));
extern size_t mbstowcs (wchar_t *__restrict __pwcs,
   const char *__restrict __s, size_t __n) __attribute__ ((__nothrow__ , __leaf__))
    __attribute__ ((__access__ (__read_only__, 2)));
extern size_t wcstombs (char *__restrict __s,
   const wchar_t *__restrict __pwcs, size_t __n)
     __attribute__ ((__nothrow__ , __leaf__))
  __attribute__ ((__access__ (__write_only__, 1, 3)))
  __attribute__ ((__access__ (__read_only__, 2)));
# 1036 "/usr/include/stdlib.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/stdlib-float.h" 1 3 4
# 1037 "/usr/include/stdlib.h" 2 3 4
# 1048 "/usr/include/stdlib.h" 3 4
# 4 "main.c" 2
# 5 "main.c"
char stack[100];
int top = -1;
int isOperator(char x) {
    switch (x) {
        case '(':
        case ')':
        case '^':
        case '%':
        case '/':
        case '*':
        case '+':
# 1 "/usr/include/x86_64-linux-gnu/bits/stdlib-float.h" 1 3 4
# 1037 "/usr/include/stdlib.h" 2 3 4
# 1048 "/usr/include/stdlib.h" 3 4
# 4 "main.c" 2
# 5 "main.c"
char stack[100];
int top = -1;
int isOperator(char x) {
    switch (x) {
        case '(':
        case ')':
        case '^':
        case '%':
        case '/':
        case '*':
        case '+':
