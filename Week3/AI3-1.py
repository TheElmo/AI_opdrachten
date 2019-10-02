import itertools, time
floors = [1,2,3,4,5]
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
	print("Lies woont op verdieping: " + str(L))
	print("Marja woont op verdieping: " + str(M))
	print("Niels woont op verdieping: " + str(N))
	print("Erik woont op verdieping: " + str(E))
	print("Joep woont op verdieping: " + str(J))