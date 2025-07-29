# Classical trial division function
def classical_trial_division(N):
    for i in range(2, int(N**0.5) + 1):
        if N % i == 0:
            return i, N // i
    return None, None

N = 21
factor1, factor2 = classical_trial_division(N)
if factor1 and factor2:
    print(f"Classical trial division found factors: {factor1} × {factor2} = {N}")