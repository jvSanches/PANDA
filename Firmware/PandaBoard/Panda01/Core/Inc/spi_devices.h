/*
 * spi_devices.h
 *
 *  Created on: Oct 27, 2020
 *      Author: joaov
 */

#ifndef INC_SPI_DEVICES_H_
#define INC_SPI_DEVICES_H_
#include "main.h"

void spiInit(SPI_HandleTypeDef *nhspix);

void digipotWrite(uint8_t ndata);

uint8_t getActiveD(void);

#endif /* INC_SPI_DEVICES_H_ */
