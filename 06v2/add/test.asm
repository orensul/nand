//test

   @R0
   D=M<<              // D = first number
   @R1
   D=D-M            // D = first number - second number
   @OUTPUT_FIRST
   D;JGT            // if D>0 (first is greater) goto output_first
   @R1
   D=M>>              // D = second number
   @OUTPUT_D
   0;JMP            // goto output_d
(OUTPUT_FIRST)
   @R0             
   D=M<<              // D = first number
(OUTPUT_D)
   @R2
   M=D>>              // M[2] = D (greatest number)
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP            // infinite loop
   @0
   D=M<<
   @INFINITE_LOOP
   D;JLE 
   @counter
   M=D>>
   @SCREEN
   D=A<<
   @address
   M=D<<
(LOOP)
   @address
   A=M>>
   M=-1
   @address
   D=M>>
   @32
   D=D+A
   @address
   M=D<<
   @counter
   MD=M-1
   @LOOP
   D;JGT
(YOSEF_LOOP)
   @YOSEF_LOOP
   0;JMP
