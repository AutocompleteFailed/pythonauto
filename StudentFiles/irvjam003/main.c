#include "stm32f0xx.h"
#include "lcd_stm32f0.h"

#define SW0 GPIO_IDR_0
#define SW1 GPIO_IDR_1
#define SW2 GPIO_IDR_2
#define SW3 GPIO_IDR_2

int minutes, seconds, miliseconds;
int button_selection;
char buffer[8];
char *frozenBuffer;

void init_ports();
void init_TIM14();
void init_NVIC();
void TIM14_IRQHandler();
void check_pb();
void display();

void main(void){

	init_ports();
	init_TIM14();
	init_NVIC();
	init_LCD();
	lcd_putstring("Stop Watch");
	lcd_command(LINE_TWO);
	lcd_putstring("Press SW0");
	GPIOB->ODR &=0b1000;

	for(;;){
		check_pb();
		TIM14_IRQHandler();
		display();
		}
}

void init_ports(void){
	RCC->AHBENR |= RCC_AHBENR_GPIOAEN;
	GPIOA->MODER &= ~(GPIO_MODER_MODER0|
					  GPIO_MODER_MODER1|
					  GPIO_MODER_MODER2|
					  GPIO_MODER_MODER3);

	GPIOA->PUPDR |= (GPIO_PUPDR_PUPDR0_0|
					 GPIO_PUPDR_PUPDR1_0|
					 GPIO_PUPDR_PUPDR2_0|
					 GPIO_PUPDR_PUPDR3_0);
	GPIOB ->MODER = 0b01010101;
	GPIOB->ODR = 0b0000000000000000;
}

void init_TIM14(){
	RCC->APB1ENR |= RCC_APB1ENR_TIM14EN;
	TIM14 -> PSC = 7;
	TIM14 -> ARR = 59999;
	TIM14 -> DIER |= TIM_DIER_UIE;
}

void init_NVIC(){
	if (SysTick_Config((uint16_t) (SystemCoreClock / 1000) - 1)) {
        	while (1);
    	}
}

void TIM14_IRQHandler(){
	int t = TIM14-> CNT;
	minutes=t/6000;
	seconds = (t%6000)/100;
	miliseconds = (t%6000)%100;
}

void check_pb(){
	if ((GPIOA->IDR &SW0)==0){
		button_selection = 0;
		TIM14->CR1|=TIM_CR1_CEN;
		GPIOB->ODR &=0b1;
	}

	if ((GPIOA->IDR &SW1)==0){
		button_selection = 1;
		frozenBuffer = buffer;
		GPIOB->ODR &=0b10;
	}

	if ((GPIOA->IDR &SW2)==0){
		button_selection = 2;
		TIM14->CR1|=TIM_CR1_CEN;
		frozenBuffer = buffer;
		GPIOB->ODR &=0b100;
	}

	if ((GPIOA->IDR &SW3)==0){
		button_selection = 3;
		TIM14->CR1&= ~TIM_CR1_CEN;
		TIM14->CNT =0x0000;
		GPIOB->ODR &=0b1000;
	}
}

void display(){
	if(button_selection==0){
		init_LCD();
		lcd_putstring("Time");
		lcd_command(LINE_TWO);
		//sprintf(buffer, "%2d:%2d.%2d",minutes,seconds,miliseconds);
		lcd_putstring(frozenBuffer);
	}

	if(button_selection==1){
		init_LCD();
		lcd_putstring("Time");
		lcd_command(LINE_TWO);
		lcd_putstring(frozenBuffer);
	}

	if(button_selection==2){
		init_LCD();
		lcd_putstring("Time");
		lcd_command(LINE_TWO);
		lcd_putstring(frozenBuffer);
	}

	if(button_selection==3){
		init_LCD();
		lcd_putstring("Time");
		lcd_command(LINE_TWO);
		lcd_putstring(frozenBuffer);
	}
}



