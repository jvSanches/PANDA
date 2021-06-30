/*
 * outputs.c
 *
 *  Created on: Oct 9, 2020
 *      Author: joaov
 */

#include "outputs.h"
#include "main.h"


//Board Defines
#define STATUS_LED_PORT LED_GREEN_GPIO_Port
#define STATUS_LED_PIN LED_GREEN_Pin

#define USER_LED_PORT LED_BLUE_GPIO_Port
#define USER_LED_PIN LED_BLUE_Pin


//State Variables
#define LED_OFF 0
#define LED_ON 1
#define LED_BLINKING 2

#define OUT_OFF 0
#define OUT_ON 1
#define OUT_PWM 2

uint8_t status_led = LED_OFF;
uint8_t user_led = LED_OFF;
uint16_t user_led_period = 1000;

uint8_t out1_mode = 0;
uint8_t out2_mode = 0;

uint8_t out1_duty = 0;
uint8_t out2_duty = 0;

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
 * setUserOutMode(output selection, mode)
 *
 */

TIM_HandleTypeDef *pwm_timer;

void setUserOutMode(uint8_t out, uint8_t mode){
	if (mode != OUT_ON && mode != OUT_OFF && mode != OUT_PWM ){
		return;
	}
	switch (out){
	case 1:
		out1_mode = mode;
		break;
	case 2:
		out2_mode = mode;
	}

	if (mode == OUT_PWM){

	}else{
		setUserOutDuty(out, mode * 255);
	}


}

void setUserOutDuty(uint8_t out, uint8_t duty){
	if (duty < 0 || duty > 255){
		return;
	}

	if (duty != 0 && duty!=255 && getUserOutMode(out) != OUT_PWM){
		setUserOutMode(out, OUT_PWM);
	}
	switch(out){
	case 1:
		out1_duty = duty;
		pwm_timer->Instance->CCR1 = duty;
		break;

	case 2:
		out2_duty = duty;
		pwm_timer->Instance->CCR2 = duty;
		break;
	}
}

/*
 * getUserOut(output)
 * Return the current output value
 */
uint8_t getUserOutMode(uint8_t out){
	uint8_t mode;
	switch(out){
	case 1:
		mode = out1_mode;
		break;

	case 2:
		mode = out2_mode;
		break;
	}
	return mode;
}

uint8_t getUserOutDuty(uint8_t out){
	uint8_t duty;
	switch(out){
	case 1:
		duty = out1_duty;
		break;

	case 2:
		duty = out2_duty;
		break;
	}
	return duty;
}


/*
 * outputsInit()
 * initializer for the outputs
 */
void outputsInit(TIM_HandleTypeDef *htimx, TIM_HandleTypeDef *PWMtimx){
	HAL_TIM_Base_Start_IT(htimx);
	statusLedMode(0);
	userLedMode(0);
	pwm_timer = PWMtimx;
	HAL_TIM_PWM_Start(pwm_timer, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(pwm_timer, TIM_CHANNEL_2);
	setUserOutMode(1, OUT_OFF);
	setUserOutMode(2, OUT_OFF);

}
