/*
 * panda_serial_device.h
 *
 *  Created on: Nov 2, 2020
 *      Author: joaov
 */

#ifndef INC_PANDA_SERIAL_DEVICE_H_
#define INC_PANDA_SERIAL_DEVICE_H_

#include "main.h"

void serial_ISR(UART_HandleTypeDef * huart);

#define SERIAL_QUEUE_SIZE 64
#define SERIAL_FRAME_SIZE 16

typedef struct{
	uint8_t queue[SERIAL_QUEUE_SIZE+1];
	uint8_t w_index;
	uint32_t last_add_tick;

}serialQueue;

serialQueue serial_Q;

void serial_addToQueue(serialQueue *q, uint8_t *msg, uint8_t len);

void serial_init(UART_HandleTypeDef * huartx);

uint8_t serial_getQueuedCommand(serialQueue *q);

void serialController(void);



#endif /* INC_PANDA_SERIAL_DEVICE_H_ */
