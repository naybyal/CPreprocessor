  int _flags;
  char *_IO_read_ptr;
  char *_IO_read_end;
  char *_IO_read_base;
  char *_IO_write_base;
  char *_IO_write_ptr;
  char *_IO_write_ptr;
  char *_IO_write_end;
  char *_IO_write_end;
  char *_IO_buf_base;
  char *_IO_buf_end;
  char *_IO_save_base;
  char *_IO_save_base;
  char *_IO_backup_base;
  char *_IO_save_end;
  struct _IO_marker *_markers;
  struct _IO_FILE *_chain;
  struct _IO_FILE *_chain;
  int _fileno;
  int _fileno;
  int _flags2;
  int _flags2;
  __off_t _old_offset;
  __off_t _old_offset;
  unsigned short _cur_column;
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];
  char _shortbuf[1];
  _IO_lock_t *_lock;
  __off64_t _offset;
  __off64_t _offset;
  struct _IO_codecvt *_codecvt;
  struct _IO_wide_data *_wide_data;
  struct _IO_FILE *_freeres_list;
  void *_freeres_buf;
  void *_freeres_buf;
  size_t __pad5;
  int _mode;
  char _unused2[15 * sizeof (int) - 4 * sizeof (void *) - sizeof (size_t)];
};
# 44 "/usr/include/stdio.h" 2 3 4
# 44 "/usr/include/stdio.h" 2 3 4
# 84 "/usr/include/stdio.h" 3 4
# 84 "/usr/include/stdio.h" 3 4
typedef __fpos_t fpos_t;
typedef __fpos_t fpos_t;
# 133 "/usr/include/stdio.h" 3 4
# 133 "/usr/include/stdio.h" 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/stdio_lim.h" 1 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/stdio_lim.h" 1 3 4
# 1 "/usr/include/x86_64-linux-gnu/bits/stdio_lim.h" 1 3 4
# 134 "/usr/include/stdio.h" 2 3 4
# 143 "/usr/include/stdio.h" 3 4
# 143 "/usr/include/stdio.h" 3 4
# 143 "/usr/include/stdio.h" 3 4
extern FILE *stdin;
extern FILE *stdout;
extern FILE *stderr;
extern FILE *stdout;
extern FILE *stderr;
extern int remove (const char *__filename) __attribute__ ((__nothrow__ , __leaf__));
extern int rename (const char *__old, const char *__new) __attribute__ ((__nothrow__ , __leaf__));
extern int rename (const char *__old, const char *__new) __attribute__ ((__nothrow__ , __leaf__));
# 178 "/usr/include/stdio.h" 3 4
extern int fclose (FILE *__stream);
extern int fclose (FILE *__stream);
extern int fclose (FILE *__stream);
# 188 "/usr/include/stdio.h" 3 4
extern FILE *tmpfile (void)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
# 205 "/usr/include/stdio.h" 3 4
extern FILE *tmpfile (void)
extern FILE *tmpfile (void)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
# 205 "/usr/include/stdio.h" 3 4
extern char *tmpnam (char[20]) __attribute__ ((__nothrow__ , __leaf__)) ;
# 230 "/usr/include/stdio.h" 3 4
extern int fflush (FILE *__stream);
extern char *tmpnam (char[20]) __attribute__ ((__nothrow__ , __leaf__)) ;
extern char *tmpnam (char[20]) __attribute__ ((__nothrow__ , __leaf__)) ;
# 230 "/usr/include/stdio.h" 3 4
extern int fflush (FILE *__stream);
extern int fflush (FILE *__stream);
# 258 "/usr/include/stdio.h" 3 4
extern FILE *fopen (const char *__restrict __filename,
extern FILE *fopen (const char *__restrict __filename,
extern FILE *fopen (const char *__restrict __filename,
extern FILE *fopen (const char *__restrict __filename,
      const char *__restrict __modes)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
      const char *__restrict __modes)
      const char *__restrict __modes)
      const char *__restrict __modes)
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
  __attribute__ ((__malloc__)) __attribute__ ((__malloc__ (fclose, 1))) ;
extern FILE *freopen (const char *__restrict __filename,
        const char *__restrict __modes,
        FILE *__restrict __stream) ;
