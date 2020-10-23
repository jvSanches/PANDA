/*
 * acquisition.c
 *
 *  Created on: Oct 8, 2020
 *      Author: joaov
 */
#include "acquisition.h"
#include "main.h"
#include "stm32f0xx_it.h"

uint8_t enc_pin_state = 0;
uint32_t encoder_count = 0;
uint8_t encoder_mode = ENCODER_QUADRATURE_MODE;
uint32_t encoder_pwm_duty=0;
uint32_t adc_dma_arr[3];

TIM_HandleTypeDef *pwm_timer;


uint16_t getAnalogRead(uint8_t in){
	return adc_dma_arr[in];
}

void setEncoderCount(uint32_t ncount){
	enc_pin_state = 2 * HAL_GPIO_ReadPin(ENC_A_GPIO_Port, ENC_A_Pin) + HAL_GPIO_ReadPin(ENC_B_GPIO_Port, ENC_B_Pin);
	encoder_count = ncount;
}

void setEncoderMode(uint8_t mode){
	encoder_mode = mode;
}
uint8_t getEncoderMode(){
	return encoder_mode;
}

uint32_t getEncoderCount(){
	return encoder_count;
}

void encoderController(){
	static uint32_t pwm_rising_edge = 0;
	static uint32_t pwm_duty_period = 0;
	static uint32_t pwm_period = 0;

	if(encoder_mode == ENCODER_QUADRATURE_MODE){
		uint8_t enc_pins_reading = 2 * HAL_GPIO_ReadPin(ENC_A_GPIO_Port, ENC_A_Pin) + HAL_GPIO_ReadPin(ENC_B_GPIO_Port, ENC_B_Pin);
		switch(enc_pin_state){
		case 0:
			if(enc_pins_reading == 2){
				encoder_count++;
			}else if(enc_pins_reading == 1){
				encoder_count--;
			}
			break;
		case 2:
			if(enc_pins_reading == 3){
				encoder_count++;
			}else if(enc_pins_reading == 0){
				encoder_count--;
			}
			break;
		case 3:
			if(enc_pins_reading == 1){
					encoder_count++;
				}else if(enc_pins_reading == 2){
					encoder_count--;
				}
			break;
		case 1:
			if(enc_pins_reading == 0){
					encoder_count++;
				}else if(enc_pins_reading == 3){
					encoder_count--;
				}
			break;
		}
		enc_pin_state = enc_pins_reading;
	}else if (encoder_mode == ENCODER_PWM_MODE){
		uint32_t acc_tick = pwm_timer->Instance->CNT;
		if (HAL_GPIO_ReadPin(ENC_A_GPIO_Port, ENC_A_Pin) == 1){
			pwm_period = acc_tick - pwm_rising_edge;
			pwm_rising_edge = acc_tick;


		}else{
			pwm_duty_period = acc_tick - pwm_rising_edge;
			encoder_pwm_duty = 4096 * pwm_duty_period / pwm_period;
		}
	}
}

uint32_t getEncoderDuty(){
	return encoder_pwm_duty;
}

uint8_t getUserIn(uint8_t in){
	switch(in){
	case 1:
		return HAL_GPIO_ReadPin(USER_IN1_GPIO_Port, USER_IN1_Pin);
		break;
	case 2:
		return HAL_GPIO_ReadPin(USER_IN2_GPIO_Port, USER_IN2_Pin);
		break;
	}
	return 0;
}



void acquisitionInit(ADC_HandleTypeDef* hadc, TIM_HandleTypeDef *htimx){
	HAL_ADC_Start_DMA(hadc, adc_dma_arr, 3);
	pwm_timer = htimx;
	HAL_TIM_Base_Start_IT(pwm_timer);
	setEncoderCount(0);
}
