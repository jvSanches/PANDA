/*
 * panda_modbus.h
 *
 *  Created on: Nov 4, 2020
 *      Author: joaov
 */

#ifndef INC_PANDA_MODBUS_H_
#define INC_PANDA_MODBUS_H_

#include "main.h"

#define MODBUS_READ_COIL_STATUS 1
#define MODBUS_READ_INPUT_STATUS 2
#define MODBUS_READ_HOLDING_REGISTERS 3
#define MODBUS_READ_INPUT_REGISTERS 4
#define MODBUS_WRITE_SINGLE_COIL 5
#define MODBUS_WRITE_SINGLE_REGISTER 6
#define MODBUS_WRITE_MULTIPLE_COILS 15
#define MODBUS_WRITE_MULTIPLE_REGISTERS 16

#define MODBUS_READ_COIL_STATUS_LEN 8
#define MODBUS_READ_INPUT_STATUS_LEN 8
#define MODBUS_READ_HOLDING_REGISTERS_LEN 8
#define MODBUS_READ_INPUT_REGISTERS_LEN 8
#define MODBUS_WRITE_SINGLE_COIL_LEN 8
#define MODBUS_WRITE_SINGLE_REGISTER_LEN 8
#define MODBUS_WRITE_MULTIPLE_COILS_LEN 11
#define MODBUS_WRITE_MULTIPLE_REGISTERS_LEN 13

#define MODBUS_OK 0
#define MODBUS_ILLEGAL_FUNCTION 1
#define MODBUS_ILLEGAL_DATA_ADDRESS 2
#define MODBUS_ILLEGAL_DATA_VALUE 3
#define MODBUS_SERVER_DEVICE_FAILURE 4

#define MODBUS_DEVICE_ADDRESS 0x04




uint8_t modbus_readCoilStatus(uint8_t * response, uint16_t starting_addr,uint16_t data);
uint8_t modbus_readInputStatus(uint8_t * response, uint16_t starting_addr,uint16_t data);
uint8_t modbus_readHoldingRegisters(uint8_t * response, uint16_t starting_addr,uint16_t data);
uint8_t modbus_readIputRegisters(uint8_t * response,uint16_t starting_addr,uint16_t data);
uint8_t modbus_writeSingleCoil(uint8_t * response, uint16_t starting_addr,uint16_t data);
uint8_t modbus_writeSingleRegister(uint8_t * response,uint16_t starting_addr,uint16_t data);

#endif /* INC_PANDA_MODBUS_H_ */
