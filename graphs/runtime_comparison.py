import matplotlib.pyplot as plt
import numpy as np

# Bit lengths to evaluate
bit_lengths = np.arange(8, 1048, 64)  # from 8 to 1024 bits in steps

# Time Complexity Estimations (arbitrary base scale for comparison)

# 1. Naive trial division: O(2^(n/2))
naive_time_log = [n/2 for n in bit_lengths]
naive_time = [2**t * 1e-9 for t in naive_time_log if t < 1024]

# 2. GNFS: exp((64/9 * n)^(1/3) * (log(n))^(2/3))
# GNFS estimated complexity: L_n[1/3, (64/9)^(1/3)] ~= exp( (1.923 * (n log n)^1/3) )
gnfs_time = [np.exp(1.923 * ((n * np.log(n))**(1/3))) * 1e-6 for n in bit_lengths]

# 3. Shor's algorithm (quantum): O(n^3)
shor_time = [np.log(n)**3 * 1e-6 for n in bit_lengths]

# Plotting
plt.figure(figsize=(12, 7))
plt.plot(bit_lengths, naive_time, label='Naive Trial Division (Classical)', marker='o')
plt.plot(bit_lengths, gnfs_time, label='General Number Field Sieve (Classical)', marker='s')
plt.plot(bit_lengths, shor_time, label="Shor's Algorithm (Quantum)", marker='^')

plt.axvspan(2048, 4096, color='lightcoral', alpha=0.3, label='RSA Key Range (2048–4096 bits)')

# Labels and styling
plt.yscale('log')  # Log scale for time axis
plt.xlabel('Number of Bits in N')
plt.ylabel('Estimated Time (log scale)')
plt.title('Factorization Time vs Bit Length: Classical vs Quantum')
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()
plt.show()
