import matplotlib.pyplot as plt

bit_lengths = [32, 64, 96, 128, 160, 192, 224, 256, 288]

t_gates = [1.15e6, 8.91e6, 3.02e7, 7.51e7, 1.51e8, 2.63e8, 4.2e8, 6.11e8, 8.37e8]
cnot_gates = [5.1e6, 3.96e7, 1.34e8, 3.34e8, 6.71e8, 1.16e9, 1.86e9, 2.7e9, 3.7e9]
h_gates = [4.74e4, 3.68e5, 1.25e6, 3.12e6, 6.28e6, 1.09e7, 1.74e7, 2.53e7, 3.48e7]

plt.figure(figsize=(12, 6))
plt.plot(bit_lengths, t_gates, label="T-Gates", marker='o')
plt.plot(bit_lengths, cnot_gates, label="CNOT-Gates", marker='s')
plt.plot(bit_lengths, h_gates, label="Hadamard-Gates", marker='^')
plt.title("Quantum Gate Usage vs Bit-Length of N")
plt.xlabel("Bit-Length of N")
plt.ylabel("Number of Gates")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()