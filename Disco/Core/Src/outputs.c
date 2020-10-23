/*
 * outputs.c
 *
 *  Created on: Oct 9, 2020
 *      Author: joaov
 */

#include "outputs.h"
#include "main.h"


//Board Defines
#define STATUS_LED_PORT LD5_GPIO_Port
#define STATUS_LED_PIN LD5_Pin

#define USER_LED_PORT LD6_GPIO_Port
#define USER_LED_PIN LD6_Pin

#define USER_OUT1_Pin LD4_Pin
#define USER_OUT1_GPIO_Port LD4_GPIO_Port

#define USER_OUT2_Pin LD3_Pin
#define USER_OUT2_GPIO_Port LD3_GPIO_Port

//State Variables
#define LED_OFF 0
#define LED_ON 1
#define LED_BLINKING 2

uint8_t status_led = LED_OFF;
uint8_t user_led = LED_OFF;
uint16_t user_led_period = 1000;

uint8_t userOut1 = 0;
uint8_t userOut2 = 0;

/*
 * statusLedController()
 * Called by the timer interruption to blink the status led
 */
void statusLedController(){
	if (status_led == LED_BLINKING){
		HAL_GPIO_TogglePin(STATUS_LED_PORT, STATUS_LED_PIN);
		}
}

/*
 * statusLedMode(mode)
 * Changes status led mode between off, on ou blinking
 */
void statusLedMode(uint8_t mode){
		if ( mode != status_led){
			switch(mode){
			case LED_OFF:
				HAL_GPIO_WritePin(STATUS_LED_PORT, STATUS_LED_PIN, 0);
				break;
			case LED_ON:
				HAL_GPIO_WritePin(STATUS_LED_PORT, STATUS_LED_PIN, 1);
				break;
			}
			status_led = mode;
		}
}

void statusLedOn(){
	statusLedMode(LED_ON);
}
void statusLedOff(){
	statusLedMode(LED_OFF);
}
void statusLedBlink(){
	statusLedMode(LED_BLINKING);
}

/*
 * userLedMode(mode)
 * Changes user led mode between off, on or blinking
 */
void userLedMode(uint8_t mode){
	user_led = mode;
	static uint8_t last_mode = 9;
	if (user_led != last_mode){
		switch(user_led){
		case LED_OFF:
			HAL_GPIO_WritePin(USER_LED_PORT, USER_LED_PIN, 0);
			break;
		case LED_ON:
			HAL_GPIO_WritePin(USER_LED_PORT, USER_LED_PIN, 1);
			break;
		case LED_BLINKING:
			userLedController();
		}
		last_mode = user_led;
	}
}

/*
 * getUserLedMode()
 * returns user led current mode
 */
uint8_t getUserLedMode(){
	return user_led;
}

/*
 * userLedFreq(frequency)
 * Changes user led mode 2 blinking frequency
 */
void userLedFreq(uint8_t freq){
	user_led_period = 1000/freq;
}

/*
 * getUserLedFreq()
 * returns user led current blinking frequency
 */
uint8_t getUserLedFreq(){
	return 1000/user_led_period;
}

/*
 * userLedController()
 * toggles the user led when on mode 2
 */
void userLedController(){
	static uint32_t last_toogle_time = 0;
	if (user_led == LED_BLINKING){
		uint32_t time = HAL_GetTick();
		if ( time > last_toogle_time + user_led_period){
			HAL_GPIO_TogglePin(USER_LED_PORT, USER_LED_PIN);
			last_toogle_time = time;
		}
	}
}

/*
 * userOutWrite(output selection, duty cycle)
 * sets the duty cycle for a user output pin
 */
void setUserOut(uint8_t out, uint8_t state){
	if (state != 0 && state != 1){
		return;
	}
	switch(out){
	case 1:
		userOut1 = state;
		HAL_GPIO_WritePin(USER_OUT1_GPIO_Port, USER_OUT1_Pin, userOut1);
		break;

	case 2:
		userOut2 = state;
		HAL_GPIO_WritePin(USER_OUT2_GPIO_Port, USER_OUT2_Pin, userOut2);
		break;
	}
}

/*
 * getUserOut(output)
 * Return the current output value
 */
uint8_t getUserOut(uint8_t out){
	uint8_t state;
	switch(out){
	case 1:
		state = userOut1;
		break;

	case 2:
		state = userOut2;
		break;
	}
	return state;
}

/*
 * outputsInit()
 * initializer for the outputs
 */
void outputsInit(TIM_HandleTypeDef *htimx){
	HAL_TIM_Base_Start_IT(htimx);
	statusLedMode(0);
	userLedMode(0);
	setUserOut(1, 0);
	setUserOut(2, 0);

}
