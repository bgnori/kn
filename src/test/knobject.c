
#include <stdio.h>
#include "minuint.h"
#include "knobject.h"


int main()
{
    knObject* obj;
    printf("this is knobject test.\n");
    obj = XNewObject(knObject);

    mu_assert("test hoge failed", obj);
    XDeleteknObject(obj);
    printf("done.\n");
    return 0;
}

