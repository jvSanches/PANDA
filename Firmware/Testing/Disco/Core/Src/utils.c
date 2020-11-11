/*
 * utils.c
 *
 *  Created on: Oct 11, 2020
 *      Author: joaov
 */

#include "main.h"
#include "utils.h"


//Utils functions
uint8_t get8MSB(uint16_t val){
	return val/256;
}
uint8_t get8LSB(uint16_t val){
	return val%256;
}
uint16_t get16MSB(uint32_t val){
	return val/65536;
}
uint16_t get16LSB(uint32_t val){
	return val%65536;
}



uint8_t getConfigBits(){
	uint8_t config = HAL_GPIO_ReadPin(CONFIG_BIT0_GPIO_Port, CONFIG_BIT0_Pin);
	config += 2 * HAL_GPIO_ReadPin(CONFIG_BIT1_GPIO_Port, CONFIG_BIT1_Pin);
	config += 4 * HAL_GPIO_ReadPin(CONFIG_BIT2_GPIO_Port, CONFIG_BIT2_Pin);
	config += 8 * HAL_GPIO_ReadPin(CONFIG_BIT3_GPIO_Port, CONFIG_BIT3_Pin);
	return config;
}
