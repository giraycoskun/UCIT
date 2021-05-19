#Modified Condition Decision Coverage
import re
sample = "(o1&o2|o3&-hello)&(ma|(asa7&asa1))"
prog = re.compile("[^\(\)\&\|-]+")
result = prog.findall(sample)
print(result)

