// The program input will be at R13,R14 while the result R13/R14 will be store at R15.
// The input registers will not change.
// The remainder will be discarded.
// We assume both numbers are positive and larger than 0.
// The program have a logarithmic running time  with respect to the input.
	
//psuedo code:
// i = -1
// y = RAM[13]
// x = RAM[14]
// while y >= x
// {
//       i += 1
//       x = x*2
// }
// RAM[15] = 0
// x = x/2
// if i == -1:
// 		RAM[15] = 0 
//
// while i >= 0
// {
//       if y >= x
// 			{
//          	accumlator = 1<<i
//				RAM[15] += accumlator 
//	            y -= x 
//			}
//        x = x/2
//  	  i -= 1
	
//copy the input 
// y = RAM[13] 
@R13 
D = M
@y
M = D

// x = RAM[14]
@R14
D = M
@x
M = D

//initializing i
@i
M = -1

(Init_Loop)
	// while y >= x
	@y
	D = M
	@x
	D=D-M
	@End_Init_Loop
	D;JLT
	
	@i
	M = M + 1
	@x
	M = M<<
	@Init_Loop
	0;JMP

(End_Init_Loop)

//if y < x: put 0 at the result, else Continue
//using the size of i that we raise at the Init_Loop while y >= x
@x
M = M>>
@R15
M=0
@i
D = M 
@End
D+1;JEQ

(Main_Loop)
//while i>= 0:
	@i
	D = M
	@End
	D;JLT
	@Y_BIGGER_THEN_X
	D = M
	@x
	D=D-M
	@y
	D;JGE
	(MAIN_LOOP_CONTINUE)
		// x = x/2
		@x
		M = M>>
		
		// i -= 1
		@i
		M = M - 1
		@Main_Loop
		0;JMP
		
	(Y_BIGGER_THEN_X)
	@i
	D = M
	@j //copy i so we noy change it
	M = D
	@accumlator
	M=1
	
	(CALCULATE_ACCUMLATOR) // accumlator = 1<<i
		@j
		D = M
		@ADD_ACCUMLATOR_TO_RESULT
		D;JEQ
		@accumlator
		M = M <<
		@j
		M = M - 1
		@CALCULATE_ACCUMLATOR
		0;JMP
		
	(ADD_ACCUMLATOR_TO_RESULT)
		@accumlator
		D = M
		@R15
		M = M + D
		
	//y -= x
	@x
	D = M
	@y
	M = M - D
	@MAIN_LOOP_CONTINUE
	0;JMP
(End)