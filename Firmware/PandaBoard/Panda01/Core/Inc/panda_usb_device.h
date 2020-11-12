/*
 * usb_device.h
 *
 *  Created on: Oct 9, 2020
 *      Author: joaov
 */

#ifndef INC_PANDA_USB_DEVICE_H_
#define INC_PANDA_USB_DEVICE_H_

#define USB_QUEUE_SIZE 64
#define USB_FRAME_SIZE 16

#include "stdint.h"

typedef struct{
	uint8_t queue[USB_QUEUE_SIZE+1];
	uint8_t r_index;
	uint8_t w_index;

}usbQueue;

usbQueue usb_Q;

void usb_addToQueue(usbQueue *q, uint8_t *msg, uint8_t len);

void usb_init(void);

uint8_t usb_getQueuedCommand(usbQueue *q);

void usbController(void);

#endif /* INC_PANDA_USB_DEVICE_H_ */
