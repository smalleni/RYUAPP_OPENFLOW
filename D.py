import time

while True:
	fname="/proc/net/dev"
	fh=open(fname)
	list1=list()
	def newfunction():
		for line in fh:
                        line=line.strip()
			if line.startswith("eth4"):
				splitting=line.split()
				for i in splitting:
					list1.append(i)
		

		print list1[2]
		return list1[2]
	k=newfunction()

	with open('out.txt', 'w') as f:
	    f.write(k)

	time.sleep(0.01)
