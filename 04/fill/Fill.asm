// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(LOOP)
@SCREEN
D=A
@pos // @pos = 16
M=D // pos = 16384 - here starts the screen
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

@pos // make the pixel in @pos white
A=M
M=0

@pos   // @pos will be the next pixel
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
