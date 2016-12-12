import numpy as np
a = []
with open("data.dat", 'r') as f:
	for line in f:
		a.append(float(line))
#print(a)
x = np.mean(a)
aa = [i-x for i in a]
lenaaa = len([ii for ii in aa if abs(ii) > 6])
lenaa = len(aa)
aax = np.mean(aa)
aMax = max(a)
aaMax = max(aa)
aMin = min(a)
aaMin = min(aa)
aMdn = np.median(a)
aaMdn = np.median(aa)

with open("results.out", 'w') as f:
	f.write("mean1 : {}\n".format(x))
	f.write("mean2 : {}\n".format(aax))
	f.write("max-min1 : {} - {}\n".format(aMax, aMin))
	f.write("max-min2 : {} - {}\n".format(aaMax, aaMin))
	f.write("lenTotal : {}\n".format(lenaa))
	f.write("lenGT : {}\n".format(lenaaa))
	f.write("percent : {}\n".format(float(lenaaa)/lenaa))
