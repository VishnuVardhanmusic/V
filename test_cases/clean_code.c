#include <stdio.h>
#define MAX_LIMIT 100

const int timeout = 50;

void ISR_Handler()
{
    // ISR does not print
}

int add(int a, int b)
{
    int sum = 0;
    sum = a + b;
    return sum;
}

int main()
{
    int x = 5;
    int y = 10;
    int result = add(x, y);
    printf("Result: %d\n", result);
    return 0;
}
