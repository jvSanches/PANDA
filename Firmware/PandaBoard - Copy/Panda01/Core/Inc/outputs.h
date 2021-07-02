/*
 * outputs.h
 *
 *  Created on: Oct 9, 2020
 *      Author: joaov
 */

#ifndef INC_OUTPUTS_H_
#define INC_OUTPUTS_H_

#include "stdint.h"

#include "main.h"

void statusLedController(void);
void statusLedOn(void);
void statusLedOff(void);
void statusLedBlink(void);

void userLedMode(uint8_t state);
void userLedFreq(uint8_t freq);
void userLedController();

uint8_t getUserLedMode(void);
uint8_t getUserLedFreq(void);

void setUserOut(uint8_t out, uint8_t state);
uint8_t getUserOut(uint8_t out);


void outputsInit(TIM_HandleTypeDef *htimx);


#endif /* INC_OUTPUTS_H_ */
