        const char *__restrict __modes,
        const char *__restrict __modes,
        FILE *__restrict __stream) ;
# 328 "/usr/include/stdio.h" 3 4
# 328 "/usr/include/stdio.h" 3 4
extern void setbuf (FILE *__restrict __stream, char *__restrict __buf) __attribute__ ((__nothrow__ , __leaf__));
extern int setvbuf (FILE *__restrict __stream, char *__restrict __buf,
extern void setbuf (FILE *__restrict __stream, char *__restrict __buf) __attribute__ ((__nothrow__ , __leaf__));
extern int setvbuf (FILE *__restrict __stream, char *__restrict __buf,
      int __modes, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
# 350 "/usr/include/stdio.h" 3 4
      int __modes, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
      int __modes, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
      int __modes, size_t __n) __attribute__ ((__nothrow__ , __leaf__));
# 350 "/usr/include/stdio.h" 3 4
# 350 "/usr/include/stdio.h" 3 4
extern int fprintf (FILE *__restrict __stream,
extern int fprintf (FILE *__restrict __stream,
extern int fprintf (FILE *__restrict __stream,
extern int fprintf (FILE *__restrict __stream,
      const char *__restrict __format, ...);
extern int printf (const char *__restrict __format, ...);
      const char *__restrict __format, ...);
      const char *__restrict __format, ...);
extern int printf (const char *__restrict __format, ...);
extern int printf (const char *__restrict __format, ...);
extern int sprintf (char *__restrict __s,
      const char *__restrict __format, ...) __attribute__ ((__nothrow__));
extern int vfprintf (FILE *__restrict __s, const char *__restrict __format,
extern int sprintf (char *__restrict __s,
extern int sprintf (char *__restrict __s,
extern int sprintf (char *__restrict __s,
      const char *__restrict __format, ...) __attribute__ ((__nothrow__));
extern int vfprintf (FILE *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg);
extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);
extern int vsprintf (char *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg);
       __gnuc_va_list __arg);
       __gnuc_va_list __arg);
extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);
extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);
extern int vprintf (const char *__restrict __format, __gnuc_va_list __arg);
extern int vsprintf (char *__restrict __s, const char *__restrict __format,
       __gnuc_va_list __arg) __attribute__ ((__nothrow__));
extern int snprintf (char *__restrict __s, size_t __maxlen,
       const char *__restrict __format, ...)
extern int snprintf (char *__restrict __s, size_t __maxlen,
extern int snprintf (char *__restrict __s, size_t __maxlen,
       const char *__restrict __format, ...)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 4)));
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 4)));
extern int vsnprintf (char *__restrict __s, size_t __maxlen,
        const char *__restrict __format, __gnuc_va_list __arg)
extern int vsnprintf (char *__restrict __s, size_t __maxlen,
        const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__)) __attribute__ ((__format__ (__printf__, 3, 0)));
# 415 "/usr/include/stdio.h" 3 4
extern int fscanf (FILE *__restrict __stream,
     const char *__restrict __format, ...) ;
extern int scanf (const char *__restrict __format, ...) ;
extern int sscanf (const char *__restrict __s,
     const char *__restrict __format, ...) __attribute__ ((__nothrow__ , __leaf__));
# 1 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 1 3 4
# 120 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 3 4
# 120 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 3 4
# 120 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 3 4
# 120 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 1 3 4
# 24 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 3 4
# 24 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/long-double.h" 1 3 4
# 25 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 2 3 4
# 25 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 2 3 4
# 25 "/usr/include/x86_64-linux-gnu/bits/floatn-common.h" 2 3 4
# 121 "/usr/include/x86_64-linux-gnu/bits/floatn.h" 2 3 4
# 431 "/usr/include/stdio.h" 2 3 4
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf")
                               ;
extern int scanf (const char *__restrict __format, ...) __asm__ ("" "__isoc99_scanf")
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf")
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf")
extern int fscanf (FILE *__restrict __stream, const char *__restrict __format, ...) __asm__ ("" "__isoc99_fscanf")
                               ;
                               ;
extern int scanf (const char *__restrict __format, ...) __asm__ ("" "__isoc99_scanf")
                              ;
extern int sscanf (const char *__restrict __s, const char *__restrict __format, ...) __asm__ ("" "__isoc99_sscanf") __attribute__ ((__nothrow__ , __leaf__))
                              ;
                              ;
                              ;
extern int sscanf (const char *__restrict __s, const char *__restrict __format, ...) __asm__ ("" "__isoc99_sscanf") __attribute__ ((__nothrow__ , __leaf__))
                      ;
# 459 "/usr/include/stdio.h" 3 4
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format,
                      ;
# 459 "/usr/include/stdio.h" 3 4
# 459 "/usr/include/stdio.h" 3 4
# 459 "/usr/include/stdio.h" 3 4
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format,
