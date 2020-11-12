/*
 * FIRFilter.c
 *
 *  Created on: Nov 1, 2020
 *      Author: joaov
 */


#include "FIRFilter.h"
#include "main.h"

static int16_t filter_taps[FIRFILTER_TAP_NUM] = {
		-5,-5,-7,-9,-12,-16,-21,-26,-31,-38,-45,-53,
		-62,-71,-80,-90,-100,-110,-119,-128,-136,-143,
		-149,-152,-154,-152,-148,-140,-128,-112,-91,-66,
		-35,2,44,92,146,205,271,342,418,500,586,676,770,
		867,966,1066,1167,1268,1367,1464,1559,1649,1735,
		1815,1888,1954,2012,2061,2101,2132,2152,2127,2127,
		2152,2132,2101,2061,2012,1954,1888,1815,1735,1649,
		1559,1464,1367,1268,1167,1066,966,867,770,676,586,
		500,418,342,271,205,146,92,44,2,-35,-66,-91,-112,
		-128,-140,-148,-152,-154,-152,-149,-143,-136,-128,
		-119,-110,-100,-90,-80,-71,-62,-53,-45,-38,-31,-26,
		-21,-16,-12,-9,-7,-5,-5
};///sum

void FIRFilter_init(FIRFilter* f) {
  int i;
  for(i = 0; i < FIRFILTER_TAP_NUM; ++i)
    f->history[i] = 0;
  f->last_index = 0;
}

void FIRFilter_put(FIRFilter* f, uint16_t input) {
  f->history[f->last_index++] = input;
  if(f->last_index == FIRFILTER_TAP_NUM)
    f->last_index = 0;
}

uint16_t FIRFilter_get(FIRFilter* f) {
  int32_t acc = 0;
  uint8_t index = f->last_index + 1;
  for(uint8_t i = 0; i < FIRFILTER_TAP_NUM; ++i) {
    if (index == FIRFILTER_TAP_NUM){
    	index = 0;
    }
    acc += (int32_t)f->history[index] * (int32_t)filter_taps[i];
  };
  return acc / 65536;
}
