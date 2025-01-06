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

