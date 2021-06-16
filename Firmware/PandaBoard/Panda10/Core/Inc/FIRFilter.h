/*
 * FIRFilter.h
 *
 *  Created on: Nov 1, 2020
 *      Author: joaov
 */

#ifndef FIRFILTER_H_
#define FIRFILTER_H_

/*

FIR filter designed with
 http://t-filter.appspot.com

sampling frequency: 10000 Hz

fixed point precision: 16 bits

* 0 Hz - 100 Hz
  gain = 1
  desired ripple = 5 dB
  actual ripple = n/a

* 1000 Hz - 2000 Hz
  gain = 0
  desired attenuation = -100 dB
  actual attenuation = n/a

*/
#include "main.h"

#define FIRFILTER_TAP_NUM 128

typedef struct {
  uint16_t history[FIRFILTER_TAP_NUM];
  uint8_t last_index;
} FIRFilter;

void FIRFilter_init(FIRFilter* f);
void FIRFilter_put(FIRFilter* f, uint16_t input);
uint16_t FIRFilter_get(FIRFilter* f);

#endif
