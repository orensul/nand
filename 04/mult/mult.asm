// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Idea: Do loop of RAM[1] times:
//		 Add RAM[0] to RAM[0]
// So we should decrease RAM[1] till it will be zero and then END the program
// Each iteration RAM[2] = RAM[2] + RAM[0]
// example: 6 * 3. RAM[0] = 6, RAM[1] = 3, RAM[2] = 0
// iteration 1: RAM[0] = 6, RAM[1] = 2, RAM[2] = 0+6=6
// iteration 2: RAM[0] = 6, RAM[1] = 1, RAM[2] = 6+6=12
// iteration 3: RAM[0] = 6, RAM[1] = 0, RAM[2] = 6+6+6=18
// END program because RAM[1] = 0

// psuedo code:
// RAM[2] = 0
// RAM[3] = RAM[1]
// LOOP:
//	if RAM[3] == 0 goto END
// 	RAM[2] += RAM[0]
//  RAM[3] -= 1
//  goto LOOP
// END:
// goto END

// Here is the real code:

// verify RAM[2] equal to zero in the beginning of the program 
@R2
M=0
// saves the value of RAM[1] in the beginning in RAM[3], so we will not destory RAM[1]
@R1
D=M
@R3
M=D
(LOOP)
// points to RAM[3] and check if RAM[3] == 0 then jump to the end of the program
	@R3
	D=M
	@END
	D;JEQ
// add to RAM[2] the value of RAM[0] 
	@R0
	D=M
	@R2
	M=M+D
// decrease the counter which is RAM[3] in one
	@R3
	M=M-1
// jump to LOOP label again
	@LOOP
	0;JMP
// here we end the program by infinite loop - to defense from hackers who can inject a malicous 
(END)
	@END
	0;JMP


