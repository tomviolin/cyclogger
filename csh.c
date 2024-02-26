#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>

#define true (1==1)
#define false (!true)

typedef unsigned int tick_t;

tick_t lasttick=0;
_Bool lastticked = false;

void pingme(int gpio, int level, unsigned int tick) {
	if (lastticked) {
		printf("t=%d dt=%d\n", tick, tick-lasttick);
	}
	lasttick = tick;
	lastticked = true;
	printf("%d: %d\n",tick,level);
}

void main(){

	int cfg = gpioCfgGetInternals();
	//cfg |= PI_CFG_NOSIGHANDLER;  // (1<<10)
	//gpioCfgSetInternals(cfg);
	int status = gpioInitialise();
	printf("status = %d\n", status);
	int result = gpioSetISRFunc(19,RISING_EDGE,5000, pingme);
	if (result){
		fprintf(stderr,"gpioSetISRFunc error %d\n",result);
		exit(result);
	}
	time_sleep(100);
}

