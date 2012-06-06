
#ifndef NKOBJECT_H
#define NKOBJECT_H

typedef int nkObject;

#define XNewObject(TYPE) ((TYPE*)_XNewObject((sizeof(TYPE))))
nkObject* _XNewObject(int size);
#define XDeleteObject(self) _XDeleteObject((Object*)(self))
void _XDeleteObject(nkObject* p);

#endif
