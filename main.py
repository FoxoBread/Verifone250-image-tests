import serial, sys; from PIL import Image;
Serial = serial.Serial(											#Assign serial port.
    port='/dev/ttyUSB0',										#Serial port device file.
    baudrate=9600,											#Baudrate.
    bytesize=serial.SEVENBITS,										#Data bits.
    parity=serial.PARITY_EVEN,										#Parity checking.
    stopbits=serial.STOPBITS_ONE,									#Stop bits.
    timeout=2,												#Read timeout (seconds).
    write_timeout=2,											#Write timeout.
    xonxoff=False,											#Software flow control.
    rtscts=True,											#Hardware flow control.
    dsrdtr=False											#DTR/DSR flow control.
);

def loop(DATA): #{											
	for i in range(0, len(DATA), 6): #{								#Loop through all even/odd bits of bit array (35 times).
		CHUNK = DATA[i:i+6];									#Get 6 bits of bit array.
		if len(CHUNK) < 6: CHUNK += [0] * (6 - len(CHUNK));					#If we're out of bits, pad with 0.
		BIT_VALUE = 0x40;									#Start with 1000000.
		for _i, v in enumerate(CHUNK): #{							#Loop through the 6 bits in chunk.
			if v: BIT_VALUE |= (1 << (5 - _i));						#If bit is 1, change BIT_VALUE to 1XXXXX where X is whichever bits is to be set.
		#}											#End chunk loop.
		Serial.write(bytes([BIT_VALUE]));							#Write either 1000000 if bit was 0 or 1XXXXX where X is bits of the image chunk.
	#}
#}

def main(): #{
	Serial.write(b'\x1B\x63');									#Reset printer.			0x1B, 0x63
	Serial.write(b'\x1C');										#Enter native mode.		0x1C
	Serial.write(b'\x1E');										#Enter double-width mode.	0x1E
	Serial.write(b'\x1B\x67');									#Enter dot graphics mode.	0x1B, 0x67

	IMAGE		= Image.open(sys.argv[1]).convert('1').resize([420, 420]);			#Load image as 1 bit 420x420 graphic.
	IMAGE_DATA	= list(IMAGE.getdata());							#Load raw image data.
	for Y in range(IMAGE.height): #{								#Loop through each vertical line in image.
		LINES	= [0] * 420;									#Initialise blank array for horizontal pixel.
		for X in range(IMAGE.width): #{								#Loop through each horizontal pixel in image.
			PIXEL_VALUE = IMAGE_DATA[Y * IMAGE.width+X];					#Get pixel value for given X and Y.
			if PIXEL_VALUE == 0: LINES[X] = 1;						#If pixel is black, set bit in array to 1 (black).
			else: LINES[X] = 0;								#If pixel is white, set bit in array to 0 (white).
		#}											#End horizontal loop.

		loop(LINES[0:420:2]);									#Jump to loop routine with odd bits from bit array.
		Serial.write(bytes([0x20|0x04]));							#Write terminator for odd bits to serial. Per documentation.
		
		loop(LINES[1:420:2]);									#Jump to loop routine with even bits from bit array.
		if Y == IMAGE.height - 1:	Serial.write(bytes([0x04 | 0x01 | 0x08]));		#If at end of image, write terminator exitting graphics mode.
		else:				Serial.write(bytes([0x04 | 0x01]));			#If not, write standard terminator to serial port. Per documentation.
	#}												#End vertical loop.
	
	Serial.close();											#Close serial port.
#}													#End main function.

if __name__ == '__main__': #{
	main();
#}