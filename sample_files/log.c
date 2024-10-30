#include <stdio.h>
#include <math.h>
long long int logarytm(long long int a)
{
    long long int acc = 0;
    while (a > 1)
    {
        acc++;
        a /= 2;
    }
    return acc;
}
int main()
{
    long long int a;
    scanf("%lld", &a);
    printf("%lld\n", logarytm(a));
}