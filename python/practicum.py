import usb

RQ_GET_Snare = 0
RQ_GET_Hihat = 1
RQ_GET_Crash = 2
RQ_GET_Tom = 3
RQ_GET_Ride = 4
RQ_GET_FT = 5
RQ_GET_LF = 6
RQ_GET_RF = 7

####################################
def find_mcu_boards():
    '''
    Find all Practicum MCU boards attached to the machine, then return a list
    of USB device handles for all the boards

    >>> devices = find_mcu_boards()
    >>> first_board = McuBoard(devices[0])
    '''
    boards = [dev for bus in usb.busses()
                  for dev in bus.devices
                  if (dev.idVendor,dev.idProduct) == (0x16c0,0x05dc)]
    return boards

####################################
class McuBoard:
    '''
    Generic class for accessing Practicum MCU board via USB connection.
    '''

    ################################
    def __init__(self, dev):
        self.device = dev
        self.handle = dev.open()

    ################################
    def usb_write(self, request, data=[], index=0, value=0):
        '''
        Send data output to the USB device (i.e., MCU board)
           request: request number to appear as bRequest field on the USB device
           index: 16-bit value to appear as wIndex field on the USB device
           value: 16-bit value to appear as wValue field on the USB device
        '''
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_OUT
        self.handle.controlMsg(
                reqType, request, data, value=value, index=index)

    ################################
    def usb_read(self, request, length=1, index=0, value=0):
        '''
        Request data input from the USB device (i.e., MCU board)
           request: request number to appear as bRequest field on the USB device
           length: number of bytes to read from the USB device
           index: 16-bit value to appear as wIndex field on the USB device
           value: 16-bit value to appear as wValue field on the USB device

        If successful, the method returns a tuple of length specified
        containing data returned from the MCU board.
        '''
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN
        buf = self.handle.controlMsg(
                reqType, request, length, value=value, index=index)
        return buf


####################################
class PeriBoard:

    ################################
    def __init__(self, mcu):
        self.mcu = mcu

    ################################
    def get_snare(self):

        light = self.mcu.usb_read(request=RQ_GET_Snare,length=2);
        return light[0]+(light[1]<<8)

    ################################
    def get_hihat(self):

        light = self.mcu.usb_read(request=RQ_GET_Hihat,length=2);
        return light[0]+(light[1]<<8)

    ################################
    def get_crash(self):

        light = self.mcu.usb_read(request=RQ_GET_Crash,length=2);
        return light[0]+(light[1]<<8)

    ################################
    def get_tom(self):

        light = self.mcu.usb_read(request=RQ_GET_Tom,length=2);
        return light[0]+(light[1]<<8)

    ################################
    def get_ride(self):

        light = self.mcu.usb_read(request=RQ_GET_Ride,length=2);
        return light[0]+(light[1]<<8)

    ################################
    def get_ft(self):

        light = self.mcu.usb_read(request=RQ_GET_FT,length=2);
        return light[0]+(light[1]<<8)
    
    ################################
    def get_lf(self):
        state = self.mcu.usb_read(request=RQ_GET_LF,length=1)
        return state[0] == 1
    
    ################################
    def get_rf(self):
        state = self.mcu.usb_read(request=RQ_GET_RF,length=1)
        return state[0] == 1