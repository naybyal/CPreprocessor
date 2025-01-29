#include <stdio.h>

// Function to add two numbers
int add(int a, int b) {
    return a + b;
}

// Function to subtract two numbers
int subtract(int a, int b) {
    return a - b;
}

// Function to multiply two numbers
int multiply(int a, int b) {
    return a * b;
}

// Function to divide two numbers (handles division by zero)
float divide(int a, int b) {
    if (b == 0) {
        printf("Error: Division by zero!\n");
        return 0;
    }
    return (float)a / b;
}

int main() {
    int x, y, choice;
    
    printf("Enter two numbers: ");
    scanf("%d %d", &x, &y);

    printf("Choose operation:\n");
    printf("1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide\n");
    scanf("%d", &choice);

    int result;
    float result_f;
    
    switch (choice) {
        case 1:
            result = add(x, y);
            printf("Result: %d\n", result);
            break;
        case 2:
            result = subtract(x, y);
            printf("Result: %d\n", result);
            break;
        case 3:
            result = multiply(x, y);
            printf("Result: %d\n", result);
            break;
        case 4:
            result_f = divide(x, y);
            printf("Result: %.2f\n", result_f);
            break;
        default:
            printf("Invalid choice!\n");
    }

    printf("Looping through numbers 1 to 5:\n");
    for (int i = 1; i <= 5; i++) {
        printf("%d ", i);
    }
    printf("\n");

    return 0;
}




// pgm 2
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function that takes ownership of a dynamically allocated string
void take_ownership(char *str) {
    printf("Received string: %s\n", str);
    free(str);  // Freeing the memory, as this function owns it
}

// Function that borrows a string (does not free it)
void borrow_string(const char *str) {
    printf("Borrowed string: %s\n", str);
}

int main() {
    // Allocating memory dynamically (ownership is with main)
    char *my_string = (char *)malloc(50 * sizeof(char));
    if (!my_string) {
        printf("Memory allocation failed\n");
        return 1;
    }

    strcpy(my_string, "Hello from C!");

    // Borrowing: Just passing reference, ownership remains with main
    borrow_string(my_string);

    // Ownership transfer: `take_ownership` now owns and frees the memory
    take_ownership(my_string);

    // This would cause an error because the memory was freed!
    // printf("After free: %s\n", my_string);  // UNDEFINED BEHAVIOR!

    return 0;
}



#include <stdio.h>
#include <stdlib.h>

// Function with potential buffer overflow
void unsafe_copy(char *dest, char *src) {
    int i = 0;
    while (src[i]!= '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0'; // Null-terminate the destination string
}

int main() {
    char source = "This is a long string that might cause an overflow!";
    char destination; // Small buffer

    unsafe_copy(destination, source); 

    printf("Copied string: %s\n", destination); 

    return 0;
}