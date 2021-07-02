/*
 * panda_i2c.c
 *
 *  Created on: Nov 1, 2020
 *      Author: joaov
 */
#include <panda_utils.h>
#include "main.h"
#include "acquisition.h"
#include "outputs.h"

#define I2C_BUFFER_SIZE 8
uint8_t i2cRXBuf[I2C_BUFFER_SIZE];
uint8_t i2cTXBuf[I2C_BUFFER_SIZE];


#define I2C_COM_IDLE 0
#define I2C_COM_WRITE 1
#define I2C_COM_READ 2

uint8_t i2c_req_n;
uint8_t i2c_res_n;
uint8_t i2c_com_state = I2C_COM_IDLE;
I2C_HandleTypeDef *hi2c;

void i2cEnable(){
	HAL_I2C_Slave_Receive_IT(hi2c, i2cRXBuf , 1);
}
void i2cInit(I2C_HandleTypeDef * hi2cx){
	hi2c = hi2cx;
	for (uint8_t i = 0; i < I2C_BUFFER_SIZE; i++){
		i2cRXBuf[i] = 0;
		i2cTXBuf[i] = 0;
	}
	i2c_com_state = I2C_COM_IDLE;
	//i2cEnable();
}

void i2cProcessRequest(){
	static uint8_t req_register;
	uint16_t res_val;
	uint32_t value ;

	if (i2c_com_state == I2C_COM_WRITE){
		switch (req_register){
		case 11:
			value = i2cRXBuf[0];
			userLedMode((uint8_t)value);
			break;
		}
		i2c_com_state = I2C_COM_IDLE;
	}else{
		req_register = i2cRXBuf[0];
		switch (req_register){
			case 11:
				i2c_com_state = I2C_COM_WRITE;
				i2c_req_n = 1;
				break;
			case 20:
				i2c_com_state = I2C_COM_READ;
				i2c_res_n = 2;
				res_val = getFromFilter();
				i2cTXBuf[0] = get8MSB(res_val);
				i2cTXBuf[1] = get8LSB(res_val);
				break;
			default:
				break;

		}
	}
	for (uint8_t i = 0; i < I2C_BUFFER_SIZE; i++){
		i2cRXBuf[i] = 0;
	}
	if (i2c_com_state == I2C_COM_READ){
		HAL_I2C_Slave_Transmit(hi2c, i2cTXBuf, i2c_res_n, 1);
		i2c_com_state = I2C_COM_IDLE;
	}
}
void i2cController(){
	switch (i2c_com_state ){
	case I2C_COM_IDLE:
		HAL_I2C_Slave_Receive(hi2c, i2cRXBuf, 1, 1);
		if (i2cRXBuf[0]){
			i2cProcessRequest();
		}
		break;
	case I2C_COM_WRITE:
		HAL_I2C_Slave_Receive(hi2c, i2cRXBuf, i2c_req_n, 1);
		i2cProcessRequest();
		break;

	}

}
