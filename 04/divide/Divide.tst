
// File name: projects/04/mult/Mult.tst

load Divide.asm,
output-file Divide.out,
compare-to Divide.cmp,
output-list RAM[13]%D2.6.2 RAM[14]%D2.6.2 RAM[15]%D2.6.2;

set RAM[13] 12,   // Set test arguments
set RAM[14] 2,
set RAM[15] -1;  // Test that program initialized product to 0
repeat 200 {
  ticktock;
}
output;

set PC 0,
set RAM[13] 1,   // Set test arguments
set RAM[14] 1,
set RAM[15] -1;  // Test that program initialized product to 0
repeat 200 {
  ticktock;
}
output;

set PC 0,
set RAM[13] 1,   // Set test arguments
set RAM[14] 3,
set RAM[15] -1;  // Test that program initialized product to 0
repeat 200 {
  ticktock;
}
output;


set PC 0,
set RAM[13] 53,   // Set test arguments
set RAM[14] 2,
set RAM[15] -1;  // Test that program initialized product to 0
repeat 300 {
  ticktock;
}
output;



set PC 0,
set RAM[13] 43,   // Set test arguments
set RAM[14] 3,
set RAM[15] -1;  // Test that program initialized product to 0
repeat 300 {
  ticktock;
}
output;