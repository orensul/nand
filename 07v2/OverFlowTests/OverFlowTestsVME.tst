// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/MemoryAccess/PointerTest/PointerTestVME.tst

load,
output-file OverFlowTests.out,
compare-to OverFlowTests.cmp,
output-list RAM[3000]%D1.6.1 RAM[3001]%D1.6.1 RAM[3002]%D1.6.1 RAM[3003]%D1.6.1 RAM[3004]%D1.6.1
            RAM[3005]%D1.6.1 RAM[3006]%D1.6.1 RAM[3007]%D1.6.1 RAM[3008]%D1.6.1 RAM[3009]%D1.6.1
            RAM[3010]%D1.6.1 RAM[3011]%D1.6.1 RAM[3012]%D1.6.1 RAM[3013]%D1.6.1 RAM[3014]%D1.6.1
            RAM[3015]%D1.6.1 RAM[3016]%D1.6.1 RAM[3017]%D1.6.1;


repeat 300 {
  vmstep;
}

// outputs the stack base, this, that, and
// some values from the the this and that segments
output;
