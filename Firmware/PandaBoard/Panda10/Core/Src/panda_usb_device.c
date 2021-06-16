/*
 * usb_device.c
 *
 *  Created on: Oct 9, 2020
 *      Author: joaov
 */

#include "panda_utils.h"
#include "panda_usb_device.h"
#include "main.h"
#include "outputs.h"
#include "usbd_cdc_if.h"
#include "acquisition.h"
#include "spi_devices.h"

uint8_t usb_active = 0;

void setUsbActive(uint8_t value){
	usb_active = value;
	if (usb_active == 1){
		statusLedOn();
	}else{
		statusLedOff();
	}
}
uint8_t getUsbActive(){
	return usb_active;
}
void usb_queueInit(usbQueue *q){
	for(uint8_t i = 0; i < USB_QUEUE_SIZE+1; i++){
		q->queue[i] = 0;
	}
	q->r_index = 0;
	q->w_index = 0;
}

void usb_init(){
	usb_queueInit(&usb_Q);
	statusLedBlink();
	setUsbActive(0);
}
/*
 * usb_addToQueue(pointer to queue, pointer to message, length of message)
 * if there is room in the queue, adds  the message to it
 * else, discards message
 */
void usb_addToQueue(usbQueue *q, uint8_t *msg, uint8_t len){
	//checks if there is room for len number in the queue
	uint8_t available_size = q->r_index + USB_QUEUE_SIZE - q->w_index;
	if(available_size > USB_QUEUE_SIZE){
		available_size = available_size - (USB_QUEUE_SIZE+1); //happens when read is "ahead" of Write
	}
	if (len <= available_size){                            //There is space
		for(uint8_t i = 0; i< len; i++){
			q->queue[q->w_index++] = msg[i];
			if (q->w_index == USB_QUEUE_SIZE+1){
				q->w_index = 0;
			}
		}
	}
}

/*
 * usb_queuedData(pointer to queue)
 * returns True if there is data  to be read in the queue
 */
uint8_t usb_queuedData(usbQueue *q){
	return (q->w_index != q->r_index);
}


/*
 * usb_peekQueue(pointer to queue, relative position)
 * returns a queue element at a relative position from the read index. Does not change the index itself
 */
uint8_t usb_peekQueue(usbQueue *q, uint8_t pos){
	uint8_t ind = q->r_index + pos;
	if (ind > (USB_QUEUE_SIZE)){
		ind = ind - (USB_QUEUE_SIZE+1);
	}
	return q->queue[ind];
}

/*
 * usb_GetByteFromQueue(pointer to queue)
 * returns a single byte from the queue
 */
uint8_t usb_GetByteFromQueue(usbQueue *q){
	uint8_t return_byte = q->queue[q->r_index];
	if (q->r_index == USB_QUEUE_SIZE){
		q->r_index = 0;
	}else{
		q->r_index++;
	}
	return return_byte;
}

/*
 * usb_queueDiscard(pointer to queue)
 * discards data until (including) next frame ending
 * return the amount of discarded numbers
 * if no frame ending is found, clears the entire queue
 */
uint8_t usb_queueDiscard(usbQueue *q){;
	for (uint8_t i =2; i< USB_QUEUE_SIZE; i++){
		if (usb_peekQueue(q, i-2) == '\r' && usb_peekQueue(q, i-1) == '\n' && usb_peekQueue(q, i) == '#'){
			q->r_index = i;
			return (i+2);
		}
	}
	q->r_index = 0;
	q->w_index = 0;
	return (USB_QUEUE_SIZE);
}

/*
 * Decodes a valid usb frame into device functions
 */
uint8_t usb_processFrame(uint8_t *frame){
	static uint8_t response[USB_FRAME_SIZE];
	response[0] = '#';
	uint8_t n = frame[1];
	UNUSED(n);
	uint8_t func = frame[2];
	uint16_t value = 0;
	uint8_t res_n = 0;
	uint16_t res_val = 0;
	uint32_t res_val32 = 0;
	uint32_t value32 = 0;
	switch (func){
	case 1://Hello
		res_n = 13;
		response[2] = 129;
		response[3] = 'I';response[4] = ' ';response[5] = 'a';response[6] = 'm';response[7] = ' ';response[8] = 'a';
		response[9] = ' ';response[10] = 'P';response[11] = 'a';response[12] = 'n';response[13] = 'd';response[14] = 'a';
		break;


	case 5://Set usb active
		value = frame[3];
		setUsbActive(value);
	case 6://get usb active
		res_n = 2;
		response[2] = 134;
		response[3] = getUsbActive(value);
		break;

	case 10://Set user led mode
		value = frame[3];
		userLedMode(value);
	case 11://Get user led mode
		res_n = 2;
		response[2] = 139;
		response[3] = getUserLedMode();
		break;

	case 12://Set user Led mode 2 Freq
		value = frame[3];
		userLedFreq(value);
	case 13://Get user led mode 2 Freq
		res_n = 2;
		response[2] = 141;
		response[3] = getUserLedFreq();
		break;

	case 14://Set user IO Out 1
		value = frame[3];
		setUserOut(1, value);
	case 15://Get user out 1
		res_n = 2;
		response[2] = 143;
		response[3] = getUserOut(1);
		break;

	case 16://Set user IO Out 2
		value = frame[3];
		setUserOut(2, value);
	case 17://Get user out 2
		res_n = 2;
		response[2] = 145;
		response[3] = getUserOut(2);
		break;

	case 20://Read analog in 2 (amp)
		res_n = 3;
		response[2] = 148;
		res_val = getFromFilter();
		response[3] = get8MSB(res_val);
		response[4] = get8LSB(res_val);
		break;

	case 21://Read user analog in 1
		res_n = 3;
		response[2] = 149;
		res_val = getAnalogRead(0);
		response[3] = get8MSB(res_val);
		response[4] = get8LSB(res_val);
		break;

	case 22://Read user analog in 2
		res_n = 3;
		response[2] = 150;
		res_val = getAnalogRead(1);
		response[3] = get8MSB(res_val);
		response[4] = get8LSB(res_val);
		break;

//	case 30://read user input 1
//		res_n = 2;
//		response[2] = 158;
//		response[3] = getUserIn(1);
//		break;
//
//	case 31://read user input 2
//		res_n = 2;
//		response[2] = 159;
//		response[3] = getUserIn(2);
//		break;

//	case 40://Set encoder mode
//		value = frame[3];
//		setEncoderMode(value);
//	case 41://Get encoder mode
//		res_n = 2;
//		response[2] = 169;
//		response[3] = getEncoderMode();
//		break;

	case 42://set encoder count
		value32 = (frame[3]<<24) + (frame[4]<<16) + (frame[5]<<8) + frame[6];
		setEncoderCount(value32);
	case 43://get encoder
		res_n = 5;
		response[2] = 171;
		res_val32 = getEncoderCount();
		response[3] = get8MSB(get16MSB(res_val32));
		response[4] = get8LSB(get16MSB(res_val32));
		response[5] = get8MSB(get16LSB(res_val32));
		response[6] = get8LSB(get16LSB(res_val32));
		break;

//	case 44:// get pwm duty cycle
//		res_n = 3;
//		response[2] = 172;
//		res_val = getEncoderDuty();
//		response[3] = get8MSB(res_val);
//		response[4] = get8LSB(res_val);
//		break;

	case 50://Calibrate Gain
		calibrateGain();
	case 51:
		res_n = 2;
		response[2] = 179;
		response[3] = getGainCalibrated();
		break;

	case 52://get RG step
		res_n = 2;
		response[2] = 180;
		response[3] = getRgStep();
		break;

	case 53://get RG wiper
		res_n = 2;
		response[2] = 181;
		response[3] = getRgWiper();
		break;

	case 54://Set amp gain
		value = (frame[3]<<8) + frame[4];
		setGain(value);
	case 55://get amp gain
		res_n = 3;
		response[2] = 183;
		res_val = getActiveGain();
		response[3] = get8MSB(res_val);
		response[4] = get8LSB(res_val);
		break;

	case 60://set offset
		value = (frame[3]<<8) + frame[4];
		setOffset(value);

	case 61: //get offset
		res_n = 3;
		response[2] = 189;
		res_val = getOffset();
		response[3] = get8MSB(res_val);
		response[4] = get8LSB(res_val);
		break;

	case 62: // auto offset
		res_val = autoOffset();
		res_n = 2;
		response[2] = 190;
		response[3] = res_val;
		break;


		//// development functions
	case 100://Set digipot
		value = frame[3];
		digipotWrite(value);
	case 101://Get last sent digipot data
		res_n = 2;
		response[2] = 229;
		response[3] = getActiveD();


	default://returns an error
		res_n = 2;
		response[2] = 0;
		response[3] = 1;
		break;

	}


	response[2 + res_n] = '\r';
	response[2 + res_n + 1] = '\n';
	response[1] = res_n;
	CDC_Transmit_FS(response, res_n + 4);
	return 0;
}

/*
 * usb_getQueuedCommand(pointer to queue)
 * Get a entire frame from the queue and verify its format,
 * If valid, it gets processed and returns 1. otherwise, returns 0 *
 */
uint8_t usb_getQueuedCommand(usbQueue *q){
	static uint8_t rx_frame[USB_FRAME_SIZE];
	if (q->queue[q->r_index] != '#'){
		usb_queueDiscard(q);
	}
	if (usb_queuedData(q)){
		uint8_t n = usb_peekQueue(q, 1);
		uint8_t frame_len = 2 + n + 2;
		for (uint8_t i = 0; i< frame_len; i++){
			rx_frame[i] = usb_GetByteFromQueue(q);
		}
		if (rx_frame[frame_len-2] == '\r' && rx_frame[frame_len-1] == '\n'){
			usb_processFrame(rx_frame);
			return 1;
		}
	}
	return 0;
}

void usbController(){
	if (usb_queuedData(&usb_Q)){
		usb_getQueuedCommand(&usb_Q);
	}
}
