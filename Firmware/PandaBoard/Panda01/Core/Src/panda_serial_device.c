/*
 * panda_serial_device.c
 *
 *  Created on: Nov 2, 2020
 *      Author: joaov
 */
#include "panda_utils.h"
#include "main.h"
#include "panda_serial_device.h"
#include "outputs.h"
#include "acquisition.h"
#include "panda_modbus.h"

uint8_t modbus_device_address = MODBUS_DEVICE_ADDRESS;

UART_HandleTypeDef * huart;


void serial_receiveEnable(){
	HAL_GPIO_WritePin(SERIAL_RSE_GPIO_Port, SERIAL_RSE_Pin, 0);
	SET_BIT(huart->Instance->CR1, USART_CR1_PEIE | USART_CR1_RXNEIE);

}
void serial_transmit(uint8_t *buf, uint8_t len){
	HAL_GPIO_WritePin(SERIAL_RSE_GPIO_Port, SERIAL_RSE_Pin, 1);
	HAL_UART_Transmit(huart, buf, len, 10);

}

void serial_ISR(UART_HandleTypeDef * huart){
	static uint8_t rxBuff[4];
	uint8_t data;
	uint32_t isrflags   = READ_REG(huart->Instance->ISR);
	uint32_t cr1its     = READ_REG(huart->Instance->CR1);
	//uint32_t cr3its     = READ_REG(huart->Instance->CR3);

	//uint32_t errorflags;
	//uint32_t errorcode;

	/* If no error occurs */
	//errorflags = (isrflags & (uint32_t)(USART_ISR_PE | USART_ISR_FE | USART_ISR_ORE | USART_ISR_NE | USART_ISR_RTOF));
	if (1){
		if (((isrflags & USART_ISR_RXNE) != 0U)&& ((cr1its & USART_CR1_RXNEIE) != 0U)){
			data = huart->Instance->RDR;
			rxBuff[0] = data;
			serial_addToQueue(&serial_Q, rxBuff, 1);
			return;
		}
	}
}

void serial_queueInit(serialQueue *q){
	for(uint8_t i = 0; i < SERIAL_QUEUE_SIZE+1; i++){
		q->queue[i] = 0;
	}
	q->w_index = 0;
	q->last_add_tick = 0;
}

void serial_init(UART_HandleTypeDef * huartx){
	huart = huartx;
	serial_queueInit(&serial_Q);
	serial_receiveEnable();
}

uint32_t frame_silence_time = 5;

/*
 * serial_addToQueue(pointer to queue, pointer to message, length of message)
 * if there is room in the queue, adds  the message to it
 * else, discards message
 */
void serial_addToQueue(serialQueue *q, uint8_t *msg, uint8_t len){
	//checks if there is room for len number in the queue
		if (q->w_index == SERIAL_QUEUE_SIZE+1){
			return;
		}
		for(uint8_t i = 0; i< len; i++){
			q->queue[q->w_index++] = msg[i];
		}
		q->last_add_tick = HAL_GetTick();
	}

/*
 * serial_queuedData(pointer to queue)
 * returns True if there is data  to be read in the queue
 */
uint8_t serial_queuedData(serialQueue *q){
	return (q->w_index);
}



/*
 * Decodes a valid serial frame into device functions
 */
uint8_t serial_processFrame(uint8_t * frame, uint8_t len){
	uint8_t modbus_status = MODBUS_OK;
	static uint8_t response[SERIAL_FRAME_SIZE];
	uint8_t func = frame[1];
	uint8_t res_n = 0;
	uint16_t starting_addr;
	uint16_t data;
	response[0] = modbus_device_address;
	response[1] = func;
	switch (func){
		case MODBUS_READ_COIL_STATUS:
			if (len != MODBUS_READ_COIL_STATUS_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 1 + data/8 + (data%8 != 0);
			modbus_status = modbus_readCoilStatus(&response[3], starting_addr, data);
			break;
		case MODBUS_READ_INPUT_STATUS:
			if (len != MODBUS_READ_INPUT_STATUS_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 1 + data/8 + (data%8 != 0);
			modbus_status = modbus_readInputStatus(&response[3], starting_addr, data);
			break;
		case MODBUS_READ_HOLDING_REGISTERS:
			if (len != MODBUS_READ_HOLDING_REGISTERS_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 2 * data + 1;
			modbus_status = modbus_readHoldingRegisters(&response[3], starting_addr, data);
			break;
		case MODBUS_READ_INPUT_REGISTERS:
			if (len != MODBUS_READ_INPUT_REGISTERS_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 2 * data + 1;
			modbus_status = modbus_readIputRegisters(&response[3], starting_addr, data);
			break;
		case MODBUS_WRITE_SINGLE_COIL:
			if (len != MODBUS_WRITE_SINGLE_COIL_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 4;
			modbus_status = modbus_writeSingleCoil(&response[3], starting_addr, data);
			break;
		case MODBUS_WRITE_SINGLE_REGISTER:
			if (len != MODBUS_WRITE_SINGLE_REGISTER_LEN){
				return 0;//framing error
			}
			starting_addr = 256 * frame[2] + frame[3];
			data = 256 * frame[4] + frame[5];
			res_n = 4;
			modbus_status = modbus_writeSingleRegister(&response[3], starting_addr, data);
			break;

		default:
			modbus_status = MODBUS_ILLEGAL_FUNCTION;
	}
	if (modbus_status!= MODBUS_OK){
		response[1]+=80;
		response[2] = modbus_status;
		res_n = 1;
	}
	uint16_t crc16 = calcCRC(response, 2 + res_n);
	response[2 + res_n] = get8LSB(crc16);
	response[2 + res_n + 1] = get8MSB(crc16);
	serial_transmit(response, 4 + res_n);
	return 1;
}
//



/*
 * serial_getQueuedCommand(pointer to queue)
 * Get a entire frame from the queue and verify its format,
 * If valid, it gets processed and returns 1. otherwise, returns 0 *
 */

uint8_t serial_getQueuedCommand(serialQueue *q){

	static uint8_t rx_frame[SERIAL_FRAME_SIZE];
	for (uint8_t i = 0; i< q->w_index; i++){
		rx_frame[i] = q->queue[i];
	}
	uint8_t rx_addr = rx_frame[0];
	if ((q->w_index) > 3 && (rx_addr == modbus_device_address)){
		uint16_t rx_crc = 256 * rx_frame[q->w_index-1] + rx_frame[q->w_index-2];
		uint16_t calc_crc = calcCRC(rx_frame, q->w_index-2);
		if (rx_crc == calc_crc){
			serial_processFrame(rx_frame, q->w_index);
			return 1;
		}

	}
	return 0;
}
uint8_t serial_frameReceived(serialQueue *q){
	return (HAL_GetTick() > q->last_add_tick + frame_silence_time && serial_queuedData(q));
}

void serialController(){
	if (serial_frameReceived(&serial_Q)){
		serial_getQueuedCommand(&serial_Q);
		serial_queueInit(&serial_Q);
		serial_receiveEnable();
	}
}
