
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/05/CPU-external.tst

load CPU.hdl,
output-file myTest.out,
compare-to myTest.cmp,
output-list time%S0.4.0 inM%D0.6.0 instruction%B0.16.0 reset%B2.1.2 outM%D1.6.0 writeM%B3.1.3 addressM%D0.5.0 pc%D0.5.0;


set instruction %B0000000000000010, // @2
tick, output, tock, output;

set instruction %B0011000000111001, // D=M
tick, output, tock, output;
