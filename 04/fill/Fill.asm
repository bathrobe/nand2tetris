    // try and store the either -1 or 0 as pixel variable, and use the same loop for either one (no matter what happens, it loops)
    // otherwise i am so close
    @SCREEN
    D=A
    @addr
    M=D //sets addr to the screen's base address

    @8191 //length of screen map
    D=A
    @n
    M=D

    (START)

    @i
    M=0 //i inits to zero
    @KBD //keyboard
    D=M
    (LOOP)
    @i
    D=M
    @n
    D=D-M
    @START
    D;JGT // goes back to check the value of the kbd after loop is done
    //RAM[arr+i] = -1

    // check the value of kbd now
    // this could be darken

    //get kbd in d
    @KBD
    D=M
    //go to M=-1 if kbd != 0, go to M=0 if kbd = 0
    @WHITE
    D;JEQ
    @DARK
    D;JNE
    (WHITE)
    @addr
    D=M
    @i
    A=D+M
    M=0

    // send it over dark into "iterate"
    @ITERATE
    0;JEQ

    (DARK)
    @addr
    D=M
    @i
    A=D+M
    M=-1

    //i++
    (ITERATE)
    @i
    M=M+1

    @LOOP
    0;JEQ //jump if it's equal to zero
