/*
 * panda_i2c.h
 *
 *  Created on: Nov 1, 2020
 *      Author: joaov
 */

#ifndef INC_PANDA_I2C_H_
#define INC_PANDA_I2C_H_

#include "main.h"

void i2cInit(I2C_HandleTypeDef * hi2cx);

void i2cEnable(void);

void i2cProcessRequest(void);

void i2cController(void);

#endif /* INC_PANDA_I2C_H_ */
