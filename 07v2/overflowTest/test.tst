
load test.asm,
output-file test.out,
compare-to test.cmp,
output-list RAM[256]%D1.6.1 RAM[257]%D1.6.1 RAM[258]%D1.6.1 RAM[259]%D1.6.1;

set RAM[0] 256,
set RAM[256] -2,
set RAM[257] -2,
set RAM[258] -2,
set RAM[259] -2,
repeat 5000 {
  ticktock;
}

output;
