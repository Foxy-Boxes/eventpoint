#pragma once
#include <vector>
#include <queue>
#include <cstdint>
#include "common.h"
uint64_t global_tick = 0;
std::vector<int> names_event;

int64_t random(int64_t range){
  return range;
}

struct param_structure { 
  std::vector<int> int_params;
  std::vector<bool> bool_params;
};
struct tick_event {
  uint64_t happens_at_tick;
  uint64_t event_index;
  param_structure* params;
  tick_event(uint64_t h, uint64_t e, param_structure* p):happens_at_tick(h), event_index(e), params(p) {}
bool operator <(const tick_event& t2) const{
  return happens_at_tick > t2.happens_at_tick;
}
};

struct event{
  uint64_t tick;
  uint64_t range;
};
typedef std::priority_queue<tick_event,std::vector<tick_event>> priq;
priq events;

typedef void (*dispatch_t)(priq& events);

extern dispatch_t dispatch_table[];

uint64_t next(){
  if(events.empty()) return UINT64_FALSE;
  tick_event const& ev = events.top();
  global_tick = ev.happens_at_tick;
  return ev.event_index;
}

void dispatch(uint64_t event_index){
  dispatch_table[event_index](events);
  events.pop();
}

void tick(){
  uint64_t event_index = next();
  if (UINT64_FALSE == event_index) return;
  dispatch(event_index);
}
