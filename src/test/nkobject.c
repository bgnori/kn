
#include <stdio.h>
#include "minuint.h"
#include "nkobject.h"


int main()
{
    nkObject* obj;
    printf("this is nkobject test.\n");
    obj = XNewObject(nkObject);

    mu_assert("test hoge failed", obj);
    printf("done.\n");
    return 0;
}

