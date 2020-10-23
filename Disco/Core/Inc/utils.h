/*
 * utils.h
 *
 *  Created on: Oct 11, 2020
 *      Author: joaov
 */

#ifndef INC_UTILS_H_
#define INC_UTILS_H_

//Utils functions
uint8_t get8MSB(uint16_t val);
uint8_t get8LSB(uint16_t val);
uint16_t get16MSB(uint32_t val);
uint16_t get16LSB(uint32_t val);
uint8_t getConfigBits();

#endif /* INC_UTILS_H_ */
