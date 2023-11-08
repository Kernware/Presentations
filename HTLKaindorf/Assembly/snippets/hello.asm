; hello.asm
global _start

_start:
mov rax, 0
mov rbx, 5

loop_start:
    inc rax
    cmp rax, rbx
    jl loop_start
nop
