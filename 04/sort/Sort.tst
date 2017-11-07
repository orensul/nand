load Sort.asm,
output-file Sort.out,
compare-to Sort.cmp,
output-list RAM[14]%D2.6.2 RAM[15]%D2.6.2 RAM[2048]%D2.6.2 RAM[2049]%D2.6.2 RAM[2050]%D2.6.2 RAM[2051]%D2.6.2 RAM[2052]%D2.6.2 RAM[2053]%D2.6.2 RAM[2054]%D2.6.2 RAM[2055]%D2.6.2 RAM[2056]%D2.6.2 RAM[2057]%D2.6.2 RAM[2058]%D2.6.2 RAM[2059]%D2.6.2 RAM[2060]%D2.6.2 RAM[2061]%D2.6.2 RAM[2062]%D2.6.2 RAM[2063]%D2.6.2 RAM[2064]%D2.6.2 RAM[2065]%D2.6.2;

set RAM[14] 2048,
set RAM[15] 18,
set RAM[2048] 1255,
set RAM[2049] -3016,
set RAM[2050] 1001,
set RAM[2051] -296,
set RAM[2052] 11700,
set RAM[2053] -15863,
set RAM[2054] -9973,
set RAM[2055] -6948,
set RAM[2056] 13084,
set RAM[2057] -1622,
set RAM[2058] -11993,
set RAM[2059] -10199,
set RAM[2060] 15507,
set RAM[2061] -7170,
set RAM[2062] 2475,
set RAM[2063] -13621,
set RAM[2064] -13821,
set RAM[2065] 8883;

repeat 20000 {
  ticktock;
}
output;

