@R13
D = M
@y
M = D
@R14
D = M
@x
M = D
@i
M = -1
(Init_Loop)
	@y
	D = M
	@x
	D=D-M
	@End_LOOP
	D;JLT
	@i
	M = M + 1
	@x
	M = M<<
	@Init_Loop
	0;JMP

(End_LOOP)
@x
M = M>>
@R15
M=0
@i
D = M 
@End
D+1;JEQ
(Main_Loop)
	@i
	D=M
	@End
	D;JLT
	@y
	D = M
	@x
	D=D-M
	@Condition
	D;JGE
	(Main_Loop_Continue)
	@x
	M = M>>
	@i
	M = M - 1
	@Main_Loop
	0;JMP	
(Condition)
	@i
	D = M
	@j
	M = D
	@part
	M=1
	(calc_part_of_the result)
	@j
	D = M
	@add_part_result
	D;JEQ
	@part
	M = M <<
	@j
	M = M - 1
	@calc_part_of_the result
	0;JMP
	(add_part_result)
	@part
	D = M
	@R15
	M = M + D
	@x
	D = M
	@y
	M = M - D
	@Main_Loop_Continue
	0;JMP
(End)
