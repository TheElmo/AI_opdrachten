import itertools, time
floors = [1,2,3,4,5]
L = "Loes"
M = "Marja"
N = "Niels"
E = "Erik"
J = "Joep"
t0 = time.time()
for (L,M,N,E,J) in list(itertools.permutations(floors)):
	if N+1 == M or N-1 == M:
		continue
	if J+1 == N or J-1 == N:
		continue
	if N == 1 or N == 5:
		continue
	if E < M:
		continue
	if M == 1:
		continue
	if L == 5:
		continue
	t1 = time.time()
	print((L,M,N,E,J))