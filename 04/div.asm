//psuedo code:
//i=0
//RAM[15] = 0
//Init_Loop
//	RAM[1] = RAM[14]
//	im=i*RAM[14]
// 	if (im - RAM[13]<0)
//		(Main_Loop)
//	else
//		i<<
//
//(Main_Loop)
//	if i == 1
//		goto end
//	i>>
//	if (RAM[15]+i)*RAM[14]) >0
//		goto Main_Loop
//	else 
//		RAM[15] + i
//	@end
//
@i
M=1
@R15 
M=0

//initioalises i to the smallest power of two that greater than R13/R14
(Init_Loop)
	@R14
	D = M
	@R0
	M = D
	@i
	D = M
	@R1
	M = D
 	@R2
	D = M - D
	@Main_Loop
	D;JGT
	@i
	M<<
	@End
	
(Main_Loop)
	@i
	D = M-1
	@End
	D;JEQ
	@i
	M>>
	@R15
	D = M
	@R1
	M = D
	@i
	D = M
	@R1
	M = M + D
	@R2
	D = M
	@Main_Loop
	D;JGT
	@i
	D = M
	@R15
	M = M + D
	
(End)
	@End
	0;JMP

	
	
	
	
	

	
	


