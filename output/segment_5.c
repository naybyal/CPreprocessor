      __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
      __gnuc_va_list __arg)
      __gnuc_va_list __arg)
      __gnuc_va_list __arg)
      __gnuc_va_list __arg)
      __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 1, 0))) ;
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__format__ (__scanf__, 1, 0))) ;
extern int vsscanf (const char *__restrict __s,
      const char *__restrict __format, __gnuc_va_list __arg)
extern int vsscanf (const char *__restrict __s,
extern int vsscanf (const char *__restrict __s,
extern int vsscanf (const char *__restrict __s,
extern int vsscanf (const char *__restrict __s,
      const char *__restrict __format, __gnuc_va_list __arg)
     __attribute__ ((__nothrow__ , __leaf__)) __attribute__ ((__format__ (__scanf__, 2, 0)));
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vfscanf")
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vfscanf")
extern int vfscanf (FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vfscanf")
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
     __attribute__ ((__format__ (__scanf__, 2, 0))) ;
extern int vscanf (const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vscanf")
     __attribute__ ((__format__ (__scanf__, 1, 0))) ;
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ , __leaf__))
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ , __leaf__))
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ , __leaf__))
extern int vsscanf (const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __asm__ ("" "__isoc99_vsscanf") __attribute__ ((__nothrow__ , __leaf__))
     __attribute__ ((__format__ (__scanf__, 2, 0)));
     __attribute__ ((__format__ (__scanf__, 2, 0)));
     __attribute__ ((__format__ (__scanf__, 2, 0)));
     __attribute__ ((__format__ (__scanf__, 2, 0)));
# 513 "/usr/include/stdio.h" 3 4
# 513 "/usr/include/stdio.h" 3 4
extern int fgetc (FILE *__stream);
extern int getc (FILE *__stream);
extern int getchar (void);
extern int getc (FILE *__stream);
extern int getc (FILE *__stream);
extern int getc (FILE *__stream);
extern int getc (FILE *__stream);
extern int getchar (void);
# 549 "/usr/include/stdio.h" 3 4
extern int fputc (int __c, FILE *__stream);
extern int fputc (int __c, FILE *__stream);
extern int putc (int __c, FILE *__stream);
extern int putchar (int __c);
extern int putchar (int __c);
extern int putchar (int __c);
extern int putchar (int __c);
# 592 "/usr/include/stdio.h" 3 4
# 592 "/usr/include/stdio.h" 3 4
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
extern char *fgets (char *__restrict __s, int __n, FILE *__restrict __stream)
     __attribute__ ((__access__ (__write_only__, 1, 2)));
# 605 "/usr/include/stdio.h" 3 4
     __attribute__ ((__access__ (__write_only__, 1, 2)));
     __attribute__ ((__access__ (__write_only__, 1, 2)));
     __attribute__ ((__access__ (__write_only__, 1, 2)));
     __attribute__ ((__access__ (__write_only__, 1, 2)));
# 605 "/usr/include/stdio.h" 3 4
# 605 "/usr/include/stdio.h" 3 4
# 605 "/usr/include/stdio.h" 3 4
# 605 "/usr/include/stdio.h" 3 4
extern char *gets (char *__s) __attribute__ ((__deprecated__));
# 655 "/usr/include/stdio.h" 3 4
extern char *gets (char *__s) __attribute__ ((__deprecated__));
extern char *gets (char *__s) __attribute__ ((__deprecated__));
extern char *gets (char *__s) __attribute__ ((__deprecated__));
extern char *gets (char *__s) __attribute__ ((__deprecated__));
# 655 "/usr/include/stdio.h" 3 4
# 655 "/usr/include/stdio.h" 3 4
# 655 "/usr/include/stdio.h" 3 4
# 655 "/usr/include/stdio.h" 3 4
extern int fputs (const char *__restrict __s, FILE *__restrict __stream);
extern int puts (const char *__s);
extern int puts (const char *__s);
extern int puts (const char *__s);
extern int puts (const char *__s);
extern int puts (const char *__s);
extern int ungetc (int __c, FILE *__stream);
extern int ungetc (int __c, FILE *__stream);
extern int ungetc (int __c, FILE *__stream);
extern size_t fread (void *__restrict __ptr, size_t __size,
extern size_t fread (void *__restrict __ptr, size_t __size,
extern size_t fread (void *__restrict __ptr, size_t __size,
       size_t __n, FILE *__restrict __stream) ;
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
extern size_t fwrite (const void *__restrict __ptr, size_t __size,
