// Performs a comparison-based sort running at O(n^2)


(BEGIN)
    // Init main counter to 0
    D = 0
    @16384      
    D = D - A
    
    @limit
    M = D
    
    //@i
    //M = 0
    @R14
    D = M
    @i
    M = D - 1

(LOOP_MAIN)

    //i++
    @i
    M = M + 1
    // Set c=&arr[0]-1, d=&arr[1]-1
    //@R14
    //D = M
    //@c
    //M = D

    // reset currentmax to -16383
    @limit
    D = M
    
    @currentmax
    M = D
    
    // for (i = j...
    @i
    D = M
    
    @j
    M = D

    // ...; i <= n; i++)
    @R14
    D = M
    
    @R15
    D = D + M
    
    @endaddr
    M = D
    
    @i
    //M = M + 1
    D = M - D //&endaddr - &i

    // Go to inner loop
    @LOOP_INNER
    D; JLE

    // if i > n, end loop
    @END
    D; JGT


(LOOP_INNER)

    // If at end of array, end current iteration of j inner loop
    @j
    D = M
    @endaddr
    D = M - D // &endaddr - &j
    // if j > n, inner loop is over
    @LOOP_MAIN
    D; JLE

    // if arr[c]<arr[d], swap.
    @currentmax
    //A = M
    D = M
    @j
    A = M
    D = D - M //currentmax - arr[j] < 0 <==> currentmax < arr[j]
    @SWAP
    D; JLT
    
    //j++   
    @j
    M = M + 1
    // Jump back to start of inner loop
    @LOOP_INNER
    0; JMP

(SWAP)

    // R0 saves arr[c]
    @i
    A = M
    D = M
    @temp
    M = D

    // Put arr[d] instead of arr[c]
    @j
    A = M
    D = M
    
    @i
    A = M
    M = D
    
    @currentmax
    M = D

    // Put R0 instead of arr[d]
    @temp
    D = M
    
    @j
    A = M
    M = D
    
    
    //j++   
    @j
    M = M + 1
    
    // Swap done, back to inner loop
    @LOOP_INNER
    0; JMP

(END)