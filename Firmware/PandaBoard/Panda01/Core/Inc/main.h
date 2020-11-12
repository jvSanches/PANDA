/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f0xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */
uint16_t calcCRC(uint8_t * data, uint8_t len);
/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define ANALOG_IN1_Pin GPIO_PIN_0
#define ANALOG_IN1_GPIO_Port GPIOA
#define ANALOG_IN2_Pin GPIO_PIN_1
#define ANALOG_IN2_GPIO_Port GPIOA
#define AMP_OUT_Pin GPIO_PIN_2
#define AMP_OUT_GPIO_Port GPIOA
#define SPI1_SS1_Pin GPIO_PIN_3
#define SPI1_SS1_GPIO_Port GPIOA
#define SERIAL_RSE_Pin GPIO_PIN_0
#define SERIAL_RSE_GPIO_Port GPIOB
#define USER_OUT1_Pin GPIO_PIN_1
#define USER_OUT1_GPIO_Port GPIOB
#define USER_OUT2_Pin GPIO_PIN_2
#define USER_OUT2_GPIO_Port GPIOB
#define USER_IN1_Pin GPIO_PIN_10
#define USER_IN1_GPIO_Port GPIOB
#define USER_IN2_Pin GPIO_PIN_11
#define USER_IN2_GPIO_Port GPIOB
#define ENC_B_Pin GPIO_PIN_12
#define ENC_B_GPIO_Port GPIOB
#define ENC_B_EXTI_IRQn EXTI4_15_IRQn
#define ENC_A_Pin GPIO_PIN_13
#define ENC_A_GPIO_Port GPIOB
#define ENC_A_EXTI_IRQn EXTI4_15_IRQn
#define LD2_Pin GPIO_PIN_14
#define LD2_GPIO_Port GPIOB
#define LD1_Pin GPIO_PIN_15
#define LD1_GPIO_Port GPIOB
#define USB_BUS_SENS_Pin GPIO_PIN_8
#define USB_BUS_SENS_GPIO_Port GPIOA
#define CONFIG_BIT0_Pin GPIO_PIN_15
#define CONFIG_BIT0_GPIO_Port GPIOA
#define CONFIG_BIT1_Pin GPIO_PIN_3
#define CONFIG_BIT1_GPIO_Port GPIOB
#define CONFIG_BIT2_Pin GPIO_PIN_4
#define CONFIG_BIT2_GPIO_Port GPIOB
#define CONFIG_BIT3_Pin GPIO_PIN_5
#define CONFIG_BIT3_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
