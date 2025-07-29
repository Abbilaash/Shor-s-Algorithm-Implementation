from math import gcd, isqrt
from sympy import isprime

N = 21

# Step 1: Look for numbers x such that x^2 mod N is B-smooth (only small factors)
B = 7  # Smoothness bound
smooth_relations = []

def is_B_smooth(n, B):
    n = abs(n)
    for p in range(2, B + 1):
        while n % p == 0:
            n = n // p
    return n == 1

# Step 2: Try small values of x around sqrt(N)
x_start = isqrt(N) + 1

for x in range(x_start, x_start + 30):
    fx = (x * x) % N
    if is_B_smooth(fx, B):
        smooth_relations.append((x, fx))

# Print collected smooth relations
print("Collected Smooth Relations:")
for x, fx in smooth_relations:
    print(f"x = {x}, x^2 mod {N} = {fx}")

# Step 3: Try to find pairs x1, x2 such that:
# x1^2 ≡ x2^2 mod N → (x1 - x2)(x1 + x2) ≡ 0 mod N
# So we brute force pairs here
for i in range(len(smooth_relations)):
    for j in range(i + 1, len(smooth_relations)):
        x1, fx1 = smooth_relations[i]
        x2, fx2 = smooth_relations[j]

        lhs = (x1**2) % N
        rhs = (x2**2) % N

        if lhs == rhs:
            print(f"\nFound congruence: {x1}^2 ≡ {x2}^2 mod {N}")
            factor1 = gcd(x1 - x2, N)
            factor2 = gcd(x1 + x2, N)

            if 1 < factor1 < N:
                print(f"Non-trivial factor found: {factor1}")
                print(f"Other factor: {N // factor1}")
            elif 1 < factor2 < N:
                print(f"Non-trivial factor found: {factor2}")
                print(f"Other factor: {N // factor2}")
            else:
                print("Trivial solution, retry.")
