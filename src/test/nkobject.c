
#include <stdio.h>
#include "minuint.h"
#include "first.h"


int main()
{

    printf("this is my first test.\n");
    mu_assert("test hoge failed", hoge());
    printf("done.\n");
    return 0;
}

