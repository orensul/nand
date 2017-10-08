@SCREEN
D=A
@pos // @pos = 16
M=D // pos = 16384 - here starts the screen


(LOOP)
@KBD
D=M      //Read keyboard input, if keyboard == 0 white else black
@BLACK
D;JNE

(WHITE)
@24576
D=A
@pos
D=D-M
@LOOP
D;JEQ


// make the pixel in @pos black
@pos
A=M
M=0


// @pos will be the next pixel
@pos
D=M+1
@pos
M=D

@WHITE
0;JMP


(BLACK)
@24576
D=A
@pos
D=D-M
@LOOP
D;JEQ

// make the pixel in @pos black
@pos
A=M
M=-1


// @pos will be the next pixel
@pos
D=M+1
@pos
M=D

@BLACK
0;JMP

