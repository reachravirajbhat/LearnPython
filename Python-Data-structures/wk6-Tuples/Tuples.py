name = input("Enter file:")
if len(name) < 1 : name = "mbox-short.txt"
handle = open(name)
counts = dict()
for line in handle:
    if not line.startswith("From"): continue
    if line.startswith("From:"): continue
    lst        = line.split()
    time       = lst[5]
    timeLst    = time.split(":")
    hr         = timeLst[0]
    counts[hr] = counts.get(hr, 0) + 1

for k,v in sorted(counts.items()):
    print(k, v)
