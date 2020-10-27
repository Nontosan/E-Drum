#include <avr/io.h>
#include <avr/interrupt.h>  /* for sei() */
#include <util/delay.h>     /* for _delay_ms() */
#include <avr/pgmspace.h>   /* required by usbdrv.h */

#include "peri.h"
#include "usbdrv.h"

#define RQ_GET_Snare 0
#define RQ_GET_Hihat 1
#define RQ_GET_Crash 2
#define RQ_GET_Tom 3
#define RQ_GET_Ride 4
#define RQ_GET_FT 5
#define RQ_GET_LF 6
#define RQ_GET_RF 7

/* ------------------------------------------------------------------------- */
/* ----------------------------- USB interface ----------------------------- */
/* ------------------------------------------------------------------------- */
usbMsgLen_t usbFunctionSetup(uint8_t data[8])
{
    usbRequest_t *rq = (void *)data;

    /* declared as static so they stay valid when usbFunctionSetup returns */
    //static uint8_t switch_state;
    /*
    if (rq->bRequest == RQ_SET_LED)
    {
        uint8_t led_state = rq->wValue.bytes[0];
        uint8_t led_no  = rq->wIndex.bytes[0];
        set_led(led_no, led_state);
        return 0;
    }
    */
    static uint16_t snare;
    static uint16_t hihat;
    static uint16_t crash;
    static uint16_t tom;
    static uint16_t ride;
    static uint16_t ft;
    static uint8_t lf;
    static uint8_t rf; 

    if (rq->bRequest == RQ_GET_Snare)
    {
	    snare = read_adc(PC0);
        usbMsgPtr = &snare;
        return 2;
    }

    else if (rq->bRequest == RQ_GET_Hihat)
    {
	    hihat = read_adc(PC1);
	    usbMsgPtr = &hihat;
	    return 2;
    }

    else if (rq->bRequest == RQ_GET_Crash)
    {
        crash = read_adc(PC2);
        usbMsgPtr = &crash;
        return 2;
    }

    else if (rq->bRequest == RQ_GET_Tom)
    {
        tom = read_adc(PC3);
        usbMsgPtr = &tom;
        return 2;
    }

    else if (rq->bRequest == RQ_GET_Ride)
    {
        ride = read_adc(PC4);
        usbMsgPtr = &ride;
        return 2;
    }

    else if (rq->bRequest == RQ_GET_FT)
    {
	    ft = read_adc(PC5);
	    usbMsgPtr = &ft;
	    return 2;
    }

    else if (rq->bRequest == RQ_GET_LF)
    {
	    lf = ((PIND & (1<<PD0)) == 0);
	    usbMsgPtr = &lf;
	    return 1;
    }

    else if (rq->bRequest == RQ_GET_RF)
    {
	    rf = ((PIND & (1<<PD1)) == 0);
	    usbMsgPtr = &rf;
	    return 1;
    }


    /* default for not implemented requests: return no data back to host */
    return 0;
}

/* ------------------------------------------------------------------------- */
int main(void)
{
    init_peri();

    usbInit();

    /* enforce re-enumeration, do this while interrupts are disabled! */
    usbDeviceDisconnect();
    _delay_ms(300);
    usbDeviceConnect();

    /* enable global interrupts */
    sei();

    /* main event loop */
    for(;;)
    {
        usbPoll();
    }

    return 0;
}

/* ------------------------------------------------------------------------- */