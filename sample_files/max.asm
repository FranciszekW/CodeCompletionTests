global smax
global umax
; Parameters in edi, esi registers
smax:
    cmp edi, esi
    cmovl eax, esi ; if edi < esi then return esi
    cmovnl eax, edi ; else edi
    ret ; result in eax
umax:
    cmp edi, esi
    cmovb eax, esi ; if edi < esi then return esi, b stands for BELOW
    cmovnb eax, edi ; else edi
    ret ; result in eax