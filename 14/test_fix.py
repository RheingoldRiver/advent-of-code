everything = [87, 69, 69, 69, 65, 64, 65, 63, 68]

total_cycles = 1000000000

cycles_before_repeat = 2

loop = everything[cycles_before_repeat:]
loop_len = len(loop)

num_cycles_after_first = total_cycles - cycles_before_repeat - 1

print(loop[(num_cycles_after_first % loop_len)])
