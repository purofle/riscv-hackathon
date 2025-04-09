# 计算 1+2+3+...+10，结果存入 x10
addi x10, x0, 0   # sum = 0
addi x11, x0, 1   # i = 1
addi x12, x0, 11  # 循环上限
loop:
    add x10, x10, x11  # sum += i
    addi x11, x11, 1   # i++
    blt x11, x12, loop  # if i < 11, jump to loop