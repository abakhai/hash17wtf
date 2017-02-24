"""hash trial"""
F = open("example.in", "r", encoding="ascii")
# print(F.read())
Details = F.readline()
Lines = F.read().splitlines()
print(Details)
print(Lines)
F.close()
