
#ifndef KNOBJECT_H
#define KNOBJECT_H

typedef int knObject;

#define XNewObject(TYPE) ((TYPE*)_XNewknObject((sizeof(TYPE))))
knObject* _XNewknObject(int size);
#define XDeleteknObject(self) _XDeleteknObject((knObject*)(self))
void _XDeleteknObject(knObject* p);

#endif
