/**
* The input of the extends ALU is instruction[9] and x[16],y[16].
* the output is define as follows:
* If instruction[7..8] equals 1 the the output is exactly as the ALU.
* Where instruction[5]=zx,instruction[4]=nx,...,instruction[0]=no.
* If instruction[7] equals 0 the output will be x*y and disregard the rest 
* of the instruction.
*
* If instruction[8] equals 0 the output will be shift.
* Then, if instruction[4] equals 0 it will return shift of y otherwise shift 
* of x, moreover if instruction[5] equals 0 it will return shift right 
* otherwise shift left.
**/
// psuedo code:
	//sel = instruction[4..5]
	// shifting = shiftleft x if sel == 11 
	//		 shift right y sel == 00
	//		 shift left y if sel == 01
	//		 shift right x if sel == 10
	//sel = instruction[7..8] 
    // if ()
	// out = ALUOut sel == 11 
	//		 x*y if sel == 00
	//		 x*y if sel == 01
	//		 shifOut if sel == 10
			 
			
	 
CHIP ExtendAlu{
    IN x[16],y[16],instruction[9];
    OUT out[16], 
		zr // 1 if (out == 0), 0 otherwise
        ng;// 1 if (out < 0),  0 otherwise
     
    PARTS:
	
	ShiftLeft(in = x , out = xshiftLeft)
	ShiftLeft(in = y , out = yshiftLeft)
	ShiftRight(in = x , out = xshiftRight)
	ShiftRight(in = y , out = yshiftRight)
	
	Mux4Way16(a = yshiftRight,b = yshiftLeft ,c = xshiftRight ,d = xshiftLeft , sel = instruction[4..5], out = shiftOut)
	 
	ALU(x = x, y = y, zx = instruction[5], nx = instruction[4], 
       zy = instruction[3], ny = instruction[2], f = instruction[1], no = instruction[0], 
       out = ALUOut, zr = zr, ng = ng);
		
	Mux4Way16(a = x*y ,b = x*y ,c = shiftOut ,d = ALUOut , sel = instruction[4..5], out = out)
	
	zr,ng - להכניס ל ALU את הפתרון?
	         
}
