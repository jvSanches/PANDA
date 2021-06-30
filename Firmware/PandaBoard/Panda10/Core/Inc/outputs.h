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

void setUserOutMode(uint8_t out, uint8_t mode);
uint8_t getUserOutMode(uint8_t out);
void setUserOutDuty(uint8_t out, uint8_t duty);
uint8_t getUserOutDuty(uint8_t out);

void outputsInit(TIM_HandleTypeDef *htimx,  TIM_HandleTypeDef *PWMtimx);



#endif /* INC_OUTPUTS_H_ */
