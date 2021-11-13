/*
 * acquisition.c
 *
 *  Created on: Oct 8, 2020
 *      Author: joaov
 */
#include "acquisition.h"
#include "main.h"
#include "stm32g4xx_it.h"
#include "spi_devices.h"

#define DMA_FILTER_SIZE 500

TIM_HandleTypeDef *enc_timer;

ADC_HandleTypeDef *adc_handler;
uint16_t adc_dma_arr[3*DMA_FILTER_SIZE];
DAC_HandleTypeDef *dac_handler;
uint16_t dac_val;

uint16_t getAnalogRead(uint8_t in){
	uint32_t analog_dma_avg = 0;
	for(uint32_t i = 0; i < DMA_FILTER_SIZE; i++){
		analog_dma_avg += adc_dma_arr[(3 * i) + in];
	}
	analog_dma_avg /= DMA_FILTER_SIZE;
	return analog_dma_avg;
}



void setOffset(uint16_t value){
	dac_val = value;
	HAL_DAC_SetValue(dac_handler, DAC_CHANNEL_1,DAC_ALIGN_12B_R, dac_val);
}
uint16_t getOffset(){
	return dac_val;
}


uint32_t getEncoderCount(){
	return enc_timer->Instance->CNT;
}

void setEncoderCount(uint32_t ncount){
	enc_timer->Instance->CNT = ncount;
}

void acquisitionInit(ADC_HandleTypeDef* hadcx, TIM_HandleTypeDef *htimx, DAC_HandleTypeDef* hdacx){
	adc_handler = hadcx;
	dac_handler = hdacx;
	enc_timer = htimx;

	HAL_ADC_Start_DMA(adc_handler, (uint32_t *)adc_dma_arr, 3*DMA_FILTER_SIZE);

	HAL_DAC_Start(dac_handler, DAC_CHANNEL_1);
    setOffset(2048);

    HAL_TIM_Base_Start(enc_timer);
	setEncoderCount(0);

	digipotWrite(255);//8.77K

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
	uint16_t d = (res_val - gain_res_wiper)/gain_res_step;
	if (d > 255){
		d = 255;
	}else if (d < 0){
		d = 0;
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
	int32_t noffset = 2048;
	int32_t offset_error =  (getAnalogRead(2) - 32768) / 16 ;
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
		offset_error =  (getAnalogRead(2) - 32768) / 16 ;
	}
	return 1;
}
