#include <stdio.h>

void ISR_Handler()
{
    printf("ISR triggered!\n"); // Violation G001
}

int main()
{
    int x; // Violation G003 (uninitialized)
    int result;
    result = x + 10;

    goto end; // Violation G002

    int i = 0;
    for (i = 0; i < 100; i++)
    { // Violation G004 (magic number 100)
        result += i;
    }

    // Simulate long function - Violation G005
    for (int j = 0; j < 60; j++)
    {
        result += j;
    }

end:
    printf("Result: %d\n", result);
    return 0;
}
