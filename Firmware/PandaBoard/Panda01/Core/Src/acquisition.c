/*
 * acquisition.c
 *
 *  Created on: Oct 8, 2020
 *      Author: joaov
 */
#include "acquisition.h"
#include "main.h"
#include "stm32f0xx_it.h"
#include "spi_devices.h"
#include "FIRFilter.h"

uint8_t enc_pin_state = 0;
uint32_t encoder_count = 0;
uint8_t encoder_mode = ENCODER_QUADRATURE_MODE;
uint32_t encoder_pwm_duty=0;

TIM_HandleTypeDef *pwm_timer;

ADC_HandleTypeDef *adc_handler;
uint16_t adc_dma_arr[3];
FIRFilter amp_filter;
DAC_HandleTypeDef *dac_handler;
uint16_t dac_val;


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

void setOffset(uint16_t value){
	dac_val = value;
	HAL_DAC_SetValue(dac_handler, DAC_CHANNEL_1,DAC_ALIGN_12B_R, dac_val);
}
uint16_t getOffset(){
	return dac_val;
}

void acquisitionInit(ADC_HandleTypeDef* hadcx, TIM_HandleTypeDef *htimx, DAC_HandleTypeDef* hdacx){
	adc_handler = hadcx;
	dac_handler = hdacx;
	pwm_timer = htimx;

	HAL_ADC_Start_DMA(adc_handler, (uint32_t *)adc_dma_arr, 3);
	FIRFilter_init(&amp_filter);

	HAL_DAC_Start(dac_handler, DAC_CHANNEL_1);
    setOffset(2048);

    HAL_TIM_Base_Start_IT(pwm_timer);
	setEncoderCount(0);

	digipotWrite(0);//8.77K



}
void sendToFilter(){
	FIRFilter_put(&amp_filter, adc_dma_arr[2]);
}

uint16_t getFromFilter(){
	return FIRFilter_get(&amp_filter);
}
/*
 * input_val is the actual differential voltage on the input in a 12 bit representation according to:
 * input_val = 4096 * dV/3.3
 */
uint8_t measureGain(uint16_t input_val){
	int32_t amp_out = 0;
	for (uint8_t i = 0; i<100; i++){
		amp_out += getAnalogRead(2)-2048;
		HAL_Delay(10);
	}
	amp_out /= 100;

	if (amp_out < 0){
		amp_out = -amp_out;
	}
	return amp_out/input_val;
}

/*
 * Suppose there is a good 33mV differential on the input
 */
uint8_t gain_res_step = 35;
uint8_t gain_res_wiper = 72;
uint8_t device_calibrated = 0;

void calibrateGain(){
	digipotWrite(255);
	HAL_Delay(100);
	uint32_t res1 = 100000 / (measureGain(41) - 1);
	HAL_Delay(100);
	digipotWrite(245);
	HAL_Delay(100);
	uint32_t res10 = 100000 / (measureGain(41) - 1);
	gain_res_step = (res10-res1) / 10;
	gain_res_wiper = res1 - gain_res_step;
	device_calibrated = 1;

}
uint8_t getGainCalibrated(){
	return device_calibrated;
}

uint8_t getRgStep(){
	return gain_res_step;
}
uint8_t getRgWiper(){
	return gain_res_wiper;
}


uint16_t calcGain(uint8_t d){
	uint16_t res =  gain_res_wiper + ((255-d) * gain_res_step);
	uint16_t gain = 1 + (100000/res);
	return gain;
}

void setGain(uint16_t ngain){
	uint16_t res_val = 100000/(ngain - 1);
	uint16_t d = 255 - (res_val - gain_res_wiper)/gain_res_step;
	if (d > 255){
		d = 255;
	}
	digipotWrite(d);
}

uint16_t getActiveGain(){
	return calcGain(getActiveD());
}
#define OFFSET_THRESHOLD 5
#define OFFSET_TIMEOUT 1000
uint8_t autoOffset(){//Auto offset routine
	setOffset(2048);
	int16_t noffset = 2048;
	int16_t offset_error =  getFromFilter() - 2048 ;
	uint32_t start_tick = HAL_GetTick();
	while ((offset_error < -OFFSET_THRESHOLD) | (offset_error > OFFSET_THRESHOLD)){
		if (HAL_GetTick() > start_tick + OFFSET_TIMEOUT){
			setOffset(2048);
			return 0;
		}
		noffset -= offset_error;
		if ((noffset > 4096) | (noffset < 0)){
			return 0;
		}
		setOffset(noffset);
		HAL_Delay(100);
		offset_error =  getFromFilter() - 2048 ;
	}
	return 1;
}
