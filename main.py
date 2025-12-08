import serial, sys; from PIL import Image
Serial = serial.Serial(
    port='/dev/ttyUSB0',			# Serial port.
    baudrate=9600,				# Baudrate.
    bytesize=serial.SEVENBITS,			# Data bits.
    parity=serial.PARITY_EVEN,			# Parity checking.
    stopbits=serial.STOPBITS_ONE,		# Stop bits.
    timeout=2,					# Read timeout (seconds).
    write_timeout=2,				# Write timeout.
    xonxoff=False,				# Software flow control.
    rtscts=True,				# Hardware flow control.
    dsrdtr=False				# DTR/DSR flow control.
)

def main(): #{
	Serial.write(b'\x1B\x63');		#Reset printer.			0x1B, 0x63
	Serial.write(b'\x1C');			#Enter native mode.		0x1C
	Serial.write(b'\x1E');			#Enter double-width mode.	0x1E
	Serial.write(b'\x1B\x67');		#Enter dot graphics mode.	0x1B, 0x67

	IMAGE	= Image.open(sys.argv[1]).convert('1');
	IMAGE	= IMAGE.resize([420, 200]);
	PIXELS	= list(IMAGE.getdata());

	for Y in range(IMAGE.height): #{
		LINES	= [0] * 420;
		_START	= Y * IMAGE.width;
		for X in range(IMAGE.width): #{
			_VALUE = PIXELS[_START+X]
			if _VALUE == 0: LINES[X] = 1;
			else: LINES[X] = 0;
		#}
		VALUES_ODD	= LINES[0:420:2];
		VALUES_EVEN	= LINES[1:420:2];

		for i in range(0, len(VALUES_ODD), 6): #{
			CHUNK = VALUES_ODD[i:i+6];
			if len(CHUNK) < 6: CHUNK += [0] * (6 - len(CHUNK));
			BYTE_VALUE = 0x40;
			for _INDEX, _BIT in enumerate(CHUNK):
				if _BIT: BYTE_VALUE |= (1 << (5 - _INDEX));
			Serial.write(bytes([BYTE_VALUE]));
		#}
		Serial.write(bytes([0x20|0x04]));

		for i in range(0, len(VALUES_EVEN), 6):#{
			CHUNK = VALUES_EVEN[i:i+6];
			if len(CHUNK) < 6: CHUNK += [0] * (6 - len(CHUNK));
			BYTE_VALUE = 0x40;
			for _INDEX, _BIT in enumerate(CHUNK):
				if _BIT: BYTE_VALUE |= (1 << (5 - _INDEX));
			Serial.write(bytes([BYTE_VALUE]));
		#}
		if Y == IMAGE.height - 1:	Serial.write(bytes([0x20 | 0x01 | 0x08]));
		else:				Serial.write(bytes([0x20 | 0x01]));
	#}
	Serial.close();
#}
if __name__ == '__main__':
	main()