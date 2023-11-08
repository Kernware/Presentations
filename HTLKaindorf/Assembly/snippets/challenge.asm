global _start ; challenge.asm
verify:
    push  rbp
    mov   rbp, rsp
    sub   dword [rbp + 16], 0x18
    xor   dword [rbp + 16], 0x7a69
    not   dword [rbp + 16]
    xor   dword [rbp + 16], 0x11e61
    xor   dword [rbp + 16], 0x37
    add   dword [rbp + 16], 0x26
    mov   eax, dword [rbp + 16]
    pop   rbp
    ret

 _start:
    ; TODO ...
    call verify
    mov rbx, 0xfffe8906
    cmp rax, rbx
    jne while_target
    lea rsi, [msg]
    mov rdi, 1
    mov rdx, 2
    mov rax, 1
    syscall

while_target:
    jmp while_target

msg db ':', ')', 0

