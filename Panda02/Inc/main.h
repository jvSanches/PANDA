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
  * This software component is licensed by ST under Ultimate Liberty license
  * SLA0044, the "License"; You may not use this file except in compliance with
  * the License. You may obtain a copy of the License at:
  *                             www.st.com/SLA0044
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

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define SPI_SS1_Pin GPIO_PIN_3
#define SPI_SS1_GPIO_Port GPIOA
#define SERIAL_RSE_Pin GPIO_PIN_0
#define SERIAL_RSE_GPIO_Port GPIOB
#define USER_OUT_1_Pin GPIO_PIN_1
#define USER_OUT_1_GPIO_Port GPIOB
#define USER_OUT_2_Pin GPIO_PIN_2
#define USER_OUT_2_GPIO_Port GPIOB
#define USER_IN_1_Pin GPIO_PIN_10
#define USER_IN_1_GPIO_Port GPIOB
#define USER_IN_2_Pin GPIO_PIN_11
#define USER_IN_2_GPIO_Port GPIOB
#define ENC_B_Pin GPIO_PIN_12
#define ENC_B_GPIO_Port GPIOB
#define ENC_A_Pin GPIO_PIN_13
#define ENC_A_GPIO_Port GPIOB
#define LD2_Pin GPIO_PIN_14
#define LD2_GPIO_Port GPIOB
#define LD1_Pin GPIO_PIN_15
#define LD1_GPIO_Port GPIOB
#define USB_BUS_SENS_Pin GPIO_PIN_8
#define USB_BUS_SENS_GPIO_Port GPIOA
#define ID_BIT0_Pin GPIO_PIN_15
#define ID_BIT0_GPIO_Port GPIOA
#define ID_BIT1_Pin GPIO_PIN_3
#define ID_BIT1_GPIO_Port GPIOB
#define ID_BIT2_Pin GPIO_PIN_4
#define ID_BIT2_GPIO_Port GPIOB
#define ID_BIT3_Pin GPIO_PIN_5
#define ID_BIT3_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
