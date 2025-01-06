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
