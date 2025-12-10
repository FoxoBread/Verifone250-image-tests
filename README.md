# Printing graphics on Verifone 250  

## Control codes  
The printer utilises control codes and sequences to perform various tasks.  
Control codes used in graphics printing are referred to by the manual as "terminators".  
Additional control codes are used to enter various modes, and set parameters. TODO: Expand this.  


### Terminators
This document assumes 7-bit byte length. If 8-bit bytes are to be used, bit after parity is always `0`.
|	Parity	bit	|	Always 1	|	Reserved bit - 0	|	Exit bit		|	Odd/Even bit				|	Colour bit		|	Feed bit	|
|	-		|	-		|	-			|	-			|	-					|	-			|	-		|
|	Per pyserial	|	Always `1`	|	Always `0`		|	Leave graphics mode	|	`0`: Even dots - `1`: Odd dots		|	`0`: Black - `1`: Red	|	Dot line feed	|

Example terminator sent by this program: `0x24` - `100100`  
Values are sent in hexidecimal, directly corresponding to their base-2 bits.
|	Hexidecimal	|	Base-2		|	Usage				|
|	-		|	-		|	-				|
|	`0x21`		|	`100000`	|	Even dot terminator		|
|	`0x24`		|	`100100`	|	Odd dot terminator		|
|	`0x29`		|	`101000`	|	Even dot terminator & exit	|

## Hardware serial configuration
|	Switch		|	setting	|
|	-		|	-	|
|	Baudrate	|	`9600`	|
|	Byte length	|	`7`	|
|	Parity		|	`even`	|

### DIP switch information  
#### Switch 1  
|	Parity		|		|
|	-		|	-	|
|	Even		|	`ON`	|
|	Odd		|	`OFF`	|
#### Switch 2  
|	Byte length	|		|
|	-		|	-	|
|	7-bit		|	`OFF`	|
|	8-bit		|	`ON`	|
#### Switch 3 & 4  
|	Baudrate	|	3	|	4	|
|	-		|	-	|	-	|
|	1200		|	`ON`	|	`ON`	|
|	2400		|	`ON`	|	`OFF`	|
|	4800		|	`OFF`	|	`ON`	|
|	9600		|	`OFF`	|	`OFF`	|  

Correct configuration for DIP set 1: `ON OFF OFF OFF`  

## Warning
This software is experimental.  
Its safety or functionality has not been verified.  
