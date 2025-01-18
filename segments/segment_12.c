}
char pop() {
    if (top >= 0)
        return stack[top--];
    else
        return '$';
}
int main() {
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
            else second = pop();
            first = pop();
            if (postfixForm[i] == '_') {
                printf("%s\t%c\t%c\n", "Uminus", first, second);
                push(second);
            } else {
                if (postfixForm[i] == '=') {
                    temp = pop();
                    printf("%c\t\t%c\t%c\n", postfixForm[i], first, temp);
                } else {
char pop() {
char pop() {
char pop() {
    if (top >= 0)
    if (top >= 0)
    if (top >= 0)
    if (top >= 0)
    if (top >= 0)
    if (top >= 0)
