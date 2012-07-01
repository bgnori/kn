
#include "peer.h"
#include "knobject.h"


knObject*
_XNewknObject(size)
    int size;
{
    knObject* r;
    r = (knObject*)peer_alloc(size);
    return r;
}


void 
_XDeleteknObject(p)
    knObject* p;
{
    peer_free((void*)p);
}


extern void onNewknObject(knObject* p);

knObject* 
_NewknObject(size)
    int size;
{
    knObject* r;
    r = _XNewknObject(size);
    onNewknObject(r);
    return r;
}


extern void onDeleteknObject(knObject* p);

void 
_DeleteknObject(self)
    knObject* self;
{
    onDeleteknObject(self);
    _XDeleteknObject(self);
}

