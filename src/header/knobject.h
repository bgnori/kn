
#ifndef KNOBJECT_H
#define KNOBJECT_H

typedef int knObject;

#define XNewObject(TYPE) ((TYPE*)_XNewknObject((sizeof(TYPE))))
knObject* _XNewknObject(int size);
#define XDeleteknObject(self) _XDeleteknObject((knObject*)(self))
void _XDeleteknObject(knObject* p);

/* hooks! for gc, etc */
extern void onNewknObject(knObject* p);
extern void onDeleteknObject(knObject* p);

#define NewknObject(TYPE) ((TYPE*)_NewknObject((sizeof(TYPE))))
knObject* _NewknObject(int size);
#define DeleteknObject(self) _DeleteknObject((knObject*)(self))
void _DeleteknObject(knObject* self);

#endif
