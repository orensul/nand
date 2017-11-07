// The program input will be at R14 (starting address), R15 (length of array). Don't change these registers.
// The program should sort the array starting at the address in R14 with length specified in R15.
// The sort is in descending order - the largest number at the head of the array.
// The array is allocated in the heap address 2048-16383.

// psuedo code SelectionSort
// 1. for j from start of array address to end of array address(=start of array address + size)
//  1.1 largest_index = j
//  1.2 for i from j+1 to end of array address
//      1.2.1 if A[i] > A[largest_index]
//          1.2.1.1 largest_index = i
//  1.3 SWAP(A[j], A[largest_index])



(BEGIN)
    @R14
    D=M

// j = RAM[14] - 1 = start address of array - 1
    @j
    M=D-1

// array_boundary = RAM[15]+j - 1 = start address of array + size - 1
    @R15
    D=M+D
    D=D-1
    @array_boundary
    M=D

(OUTER_LOOP)
// j++
    @j
    M=M+1

    // jump to END <-> j - array_boundary > 0 <-> j > array_boundary
    @j
    D=M
    @array_boundary
    D=D-M
    @END
    D;JGT

// largest_index = j
    @j
    D=M
    @largest_index
    M=D

// i = j
    @j
    D=M
    @i
    M=D

(INNER_LOOP)
// i++
    @i
    M=M+1

// jump to SWAP <-> i - array_boundary > 0 <-> i > array_boundary
    @i
    D=M
    @array_boundary
    D=D-M
    @SWAP
    D;JGT



// jump to UPDATE_LARGEST <-> A[largest_index] - A[i] < 0 <-> A[largest_index] < A[i]
    // D = A[largest_index]
    @largest_index
    A=M
    D=M
    // D = A[largest_index] - A[i]
    @i
    A=M
    D=D-M
    @UPDATE_LARGEST
    D;JLT

    @INNER_LOOP
    0;JMP

// psuedo code swap
// temp = arr[largest_index]
// arr[largest_index] = arr[j]
// arr[j] = temp

(SWAP)
// temp = arr[largest_index]
    @largest_index
    A=M
    D=M
    @temp
    M=D
// arr[largest_index] = arr[j]
    @j
    A=M
    D=M
    @largest_index
    A=M
    M=D

// arr[j] = temp
    @temp
    D=M
    @j
    A=M
    M=D

    @OUTER_LOOP
    0;JMP

(UPDATE_LARGEST)
    @i
    D=M
    @largest_index
    M=D
    @INNER_LOOP
    0;JMP