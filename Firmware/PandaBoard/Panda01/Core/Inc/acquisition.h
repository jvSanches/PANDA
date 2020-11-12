/*
 * acquisition.h
 *
 *  Created on: Oct 8, 2020
 *      Author: joaov
 */

#ifndef DEVICES_ACQUISITION_H_
#define DEVICES_ACQUISITION_H_

#include "main.h"

void acquisitionInit(ADC_HandleTypeDef* hadcx,  TIM_HandleTypeDef *htimx, DAC_HandleTypeDef *hdacx);

void setOffset(uint16_t value);

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

void calibrateGain(void);

void setGain(uint16_t ngain);

uint16_t getActiveGain(void);

uint8_t getRgStep(void);

uint8_t getRgWiper(void);

uint8_t getGainCalibrated(void);

void sendToFilter(void);

uint16_t getFromFilter(void);

uint8_t autoOffset(void);

void setOffset(uint16_t value);

uint16_t getOffset(void);

#endif /* DEVICES_ACQUISITION_H_ */
