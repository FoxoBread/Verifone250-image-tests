from lib import fakeSerial as Serial; from PIL import Image

def main(): #{
	Serial.write(b'\x1B\x63');		#Reset printer.			0x1B, 0x63
	Serial.write(b'\x1C');			#Enter native mode.		0x1C
	Serial.write(b'\x1E');			#Enter double-width mode.	0x1E
	Serial.write(b'\x1B\x67');		#Enter dot graphics mode.	0x1B, 0x67

	IMAGE	= Image.open('foo.bmp');
	WIDTH	= IMAGE.width;
	HEIGHT	= IMAGE.height;
	PIXELS	= list(IMAGE.getdata());

	for Y in range(HEIGHT):
		LINES	= [0] * 420;
		_START	= Y * WIDTH;
		for X in range(WIDTH): #{
			_VALUE = PIXELS[_START+X]
			if _VALUE == 0: LINES[X] = 1;
			else: LINES[X] = 0;
		#}
		VALUES_ODD	= LINES[0:420:2];
		VALUES_EVEN	= LINES[1:420:2];

		for i in range(0, len(VALUES_ODD), 6):
			CHUNK = VALUES_ODD[i:i+6];
			if len(CHUNK) < 6: CHUNK += [0] * (6 - len(CHUNK));
			BYTE_VALUE = 0x40;
			for _INDEX, _BIT in enumerate(CHUNK):
				if _BIT: BYTE_VALUE |= (1 << (5 - _INDEX));
			Serial.write(bytes([BYTE_VALUE]));
		
		Serial.write(bytes([0x20|0x04]));

		for i in range(0, len(VALUES_EVEN), 6):
			CHUNK = VALUES_EVEN[i:i+6];
			if len(CHUNK) < 6: CHUNK += [0] * (6 - len(CHUNK));
			BYTE_VALUE = 0x40;
			for _INDEX, _BIT in enumerate(CHUNK):
				if _BIT: BYTE_VALUE |= (1 << (5 - _INDEX));
			Serial.write(bytes([BYTE_VALUE]));
		
		if Y == HEIGHT - 1:	Serial.write(bytes([0x20 | 0x01 | 0x08]));
		else:			Serial.write(bytes([0x20 | 0x01]));

	Serial.close();

if __name__ == '__main__':
	main()