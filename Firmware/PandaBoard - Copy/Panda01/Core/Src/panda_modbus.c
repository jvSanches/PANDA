/*
 * panda_modbus.c
 *
 *  Created on: Nov 4, 2020
 *      Author: joaov
 */
#include "panda_modbus.h"
#include "outputs.h"
#include "acquisition.h"
#define MAX_COILS 3
#define MAX_INPUTS 2




uint8_t getCoils(uint16_t ind){
	switch (ind){
	case 0:
		return getUserLedMode();
		break;
	case 1:
		return getUserOut(1);
		break;
	case 2:
		return getUserOut(2);
		break;
	}
	return 0;
}

uint8_t getInputs(uint16_t ind){
	switch (ind){
	case 1:
		return getUserIn(1);
		break;
	case 2:
		return getUserIn(2);
		break;
	}
	return 0;
}

uint8_t writeCoil(uint16_t ind, uint8_t value){
	switch (ind){
		case 0:
			userLedMode(value);
			return 1;
			break;
		case 1:
			setUserOut(1, value);
			return 1;
			break;
		case 2:
			setUserOut(1, value);
			return 1;
			break;

		}
		return 0;
}

uint8_t modbus_readCoilStatus(uint8_t * response, uint16_t starting_addr, uint16_t data){
	if (data > MAX_COILS){
		return MODBUS_ILLEGAL_DATA_VALUE;
	}
	if (data < 1 || starting_addr + data > MAX_COILS ){
		return MODBUS_ILLEGAL_DATA_ADDRESS;
	}
	*response = data/8 + (data%8 != 0);
	response++;
	uint8_t res_byte = 0;
	for (uint8_t i = 0; i<data; i++){
		if(getCoils(starting_addr + i)){
			res_byte &= 1<<(i%8);
		}
		if ((i%8) == 7){
			*response = res_byte;
			response++;
			res_byte = 0;
		}
	}
	return MODBUS_OK;
}
uint8_t modbus_readInputStatus(uint8_t * response, uint16_t starting_addr, uint16_t data){
	if (data > MAX_INPUTS){
			return MODBUS_ILLEGAL_DATA_VALUE;
		}
	if (data < 1 || starting_addr + data > MAX_INPUTS ){
		return MODBUS_ILLEGAL_DATA_ADDRESS;
	}
	*response = data/8 + (data%8 != 0);
	response++;
	uint8_t res_byte = 0;
	for (uint8_t i = 0; i<data; i++){
		if(getInputs(starting_addr + i)){
			res_byte &= 1<<(i%8);
		}
		if ((i%8) == 7){
			*response = res_byte;
			response++;
			res_byte = 0;
		}
	}
	return MODBUS_OK;
}
uint8_t modbus_readHoldingRegisters(uint8_t * response, uint16_t starting_addr, uint16_t data){
	return MODBUS_SERVER_DEVICE_FAILURE;
}
uint8_t modbus_readIputRegisters(uint8_t * response, uint16_t starting_addr, uint16_t data){
	return MODBUS_SERVER_DEVICE_FAILURE;
}
uint8_t modbus_writeSingleCoil(uint8_t * response, uint16_t starting_addr, uint16_t data){
	if (starting_addr > MAX_COILS){
			return MODBUS_ILLEGAL_DATA_ADDRESS;
		}
	if (data != 0xFF00 && data!=0x0000 ){
		return MODBUS_ILLEGAL_DATA_VALUE;
	}
	if (writeCoil(starting_addr, (data != 0)) == 0){
		return MODBUS_SERVER_DEVICE_FAILURE;
	}
	return MODBUS_OK;
}
uint8_t modbus_writeSingleRegister(uint8_t * response, uint16_t starting_addr, uint16_t data){
	return MODBUS_SERVER_DEVICE_FAILURE;
}
