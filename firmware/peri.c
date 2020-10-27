#include <avr/io.h>
#include "peri.h"

void init_peri()
{
    // PC0,PC1,...,PC5 -> input
    DDRC &= ~((1<<PC0)|(1<<PC1)|(1<<PC2)|(1<<PC3)|(1<<PC4)|(1<<PC5));

    // PD0,PD1 -> input
    DDRD &= ~((1<<PD0)|(1<<PD1));

    // enable pull-up resistor on PD0, PD1
    PORTD |= (1<<PD0)|(1<<PD1);
}

uint16_t read_adc(uint8_t channel)
{
    ADMUX = (0<<REFS1)|(1<<REFS0) // use VCC as reference voltage
          | (0<<ADLAR)            // store result to the right of ADCH/ADCL
          | (channel & 0b1111);   // point MUX to the specified channel
 
    ADCSRA = (1<<ADEN)            // enable ADC
           | (1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0) // set speed to 1/128 of system clock
           | (1<<ADSC);           // start conversion
 
    // wait until ADSC bit becomes 0, indicating complete conversion
    while ((ADCSRA & (1<<ADSC)))
       ;
 
    return ADCL + ADCH*256;
}