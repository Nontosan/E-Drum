//#define SWITCH_PRESSED() ((PINC & (1<<PC3)) == 0)
void init_peri();
uint16_t read_adc(uint8_t channel);
