/*
 * acquisition.h
 *
 *  Created on: Oct 8, 2020
 *      Author: joaov
 */

#ifndef DEVICES_ACQUISITION_H_
#define DEVICES_ACQUISITION_H_

#include "main.h"

void acquisitionInit(ADC_HandleTypeDef* hadc,  TIM_HandleTypeDef *htimx);

uint16_t getAnalogRead(uint8_t in);

#define ENCODER_QUADRATURE_MODE 0
#define ENCODER_PWM_MODE 1

void encoderController(void);

uint32_t getEncoderDuty(void);

void setEncoderCount(uint32_t ncount);

void setEncoderMode(uint8_t mode);

uint8_t getEncoderMode(void);

uint32_t getEncoderCount(void);

uint8_t getUserIn(uint8_t in);


#endif /* DEVICES_ACQUISITION_H_ */
