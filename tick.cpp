

#include <vector>       // std::vector
#include <string>
#include "register.h"
#include "tick_event.h"


int main(){
  init();
  for(int i = 420; i< 800; i+=10){
    change_period(i,0);
    start_period(5000);
    while(events.size()){
      tick();
    }
    std::cout << (double)num_recv / (double) num_sent << std::endl;
    init();
  }
}
