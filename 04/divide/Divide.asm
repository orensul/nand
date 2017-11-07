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
	
@R13
D=M
@y
M=D
@R14
D=M
@x
M=D
@i
M=-1
(INIT_LOOP)
@y
D=M
@x
D=D-M
@END_LOOP
D;JLT
@i
M=M+1
@x
M=M<<
@INIT_LOOP
0;JMP
(END_LOOP)
@x
M=M>>
@R15
M=0
@i
D=M 
@END
D+1;JEQ
(MAIN_LOOP)
@i
D=M
@END
D;JLT
@y
D=M
@x
D=D-M
@Y_BIGGER_THAN_X
D;JGE
(MAIN_LOOP_CONTINUE)
@x
M=M>>
@i
M=M-1
@MAIN_LOOP
0;JMP	
(Y_BIGGER_THAN_X)
@i
D=M
@j
M=D
@accumulator
M=1
(CALC_ACCUMULATOR)
@j
D=M
@ADD_ACCUMULATOR
D;JEQ
@accumulator
M=M<<
@j
M=M-1
@CALC_ACCUMULATOR 
0;JMP
(ADD_ACCUMULATOR)
@accumulator
D=M
@R15
M=M+D
@x
D=M
@y
M=M-D
@MAIN_LOOP_CONTINUE
0;JMP
(END)