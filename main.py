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
		BYTE_VALUE = 0x40;									#TODO: Why 0x40?
		for i, BIT in enumerate(CHUNK): #{							#Loop through the 6 bits in chunk.
			if BIT: BYTE_VALUE |= (1 << (5 - i));						#If bit is 1, Inclusive or 0x40 with 1 bit shifted to left 5-loop iteration. TODO: Why???
		#}											#End chunk loop.
		Serial.write([BYTE_VALUE]);								#Write either 0x40 or whatever the cursed hell the above operation returned. TODO: WHY?!
	#}
#}

def main(): #{
	print(b'\x1B\x63');										#Reset printer.			0x1B, 0x63
	print(b'\x1C');											#Enter native mode.		0x1C
	print(b'\x1E');											#Enter double-width mode.	0x1E
	print(b'\x1B\x67');										#Enter dot graphics mode.	0x1B, 0x67

	IMAGE	= Image.open(sys.argv[1]).convert('1').resize([420, 420]);				#Load image as 1 bit 420x420 graphic.

	for Y in range(IMAGE.height): #{								#Loop through each vertical line in image.
		LINES	= [0] * 420;									#Initialise blank array for horizontal pixel.
		for X in range(IMAGE.width): #{								#Loop through each horizontal pixel in image.
			PIXEL_VALUE = list(IMAGE.getdata())[Y * IMAGE.width+X]				#Get pixel value for given X and Y.
			if PIXEL_VALUE == 0: LINES[X] = 1;						#If pixel is black, set bit in array to 1 (black).
			else: LINES[X] = 0;								#If pixel is white, set bit in array to 0 (white).
		#}											#End horizontal loop.

		print(bytes([0x20|0x04]));								#Write 36 "\x00"'s to serial port. TODO: Why?

		loop(LINES[0:420:2]);									#Jump to loop routine with odd bits from bit array.
		loop(LINES[1:420:2]);									#Jump to loop routine with even bits from bit array.

		if Y == IMAGE.height - 1:	Serial.write(bytes([0x20 | 0x01 | 0x08]));		#If vertical loop index equal to image Y - 1: write 0x29 to serial. TODO: Why?
		else:				Serial.write(bytes([0x20 | 0x01]));			#If not: write 0x21 to serial. TODO: Why?
	#}												#End vertical loop.
	
	Serial.close();											#Close serial port.
#}													#End main function.

if __name__ == '__main__': #{
	main();
#}