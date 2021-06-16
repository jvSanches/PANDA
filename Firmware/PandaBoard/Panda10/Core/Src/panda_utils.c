/*
 * utils.c
 *
 *  Created on: Oct 11, 2020
 *      Author: joaov
 */

#include "panda_utils.h"
#include "main.h"


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



