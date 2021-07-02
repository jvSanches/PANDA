/*
 * spi_devices.c
 *
 *  Created on: Oct 27, 2020
 *      Author: joaov
 */
#include "main.h"
#define GAIN_POT_SS_PORT SPI1_SS1_GPIO_Port
#define GAIN_POT_SS_PIN SPI1_SS1_Pin

SPI_HandleTypeDef *hspix;

uint8_t last_digipot_data;
uint8_t getActiveD(){
	return last_digipot_data;
}

void digipotWrite(uint8_t ndata){
	HAL_GPIO_WritePin(GAIN_POT_SS_PORT, GAIN_POT_SS_PIN, 0);
	HAL_Delay(50);
	uint8_t potdata[2];
	potdata[0] = 0b00010011;
	potdata[1] = ndata;
	HAL_SPI_Transmit(hspix,potdata, 2, 50);
	HAL_Delay(50);
	last_digipot_data = ndata;
	HAL_GPIO_WritePin(GAIN_POT_SS_PORT, GAIN_POT_SS_PIN, 1);

}
void spiInit(SPI_HandleTypeDef *nhspix){
	hspix = nhspix;
	digipotWrite(255);
}
