import matplotlib.pyplot as plt
import numpy as np

# Bit lengths to consider for N
bit_lengths = np.arange(4, 4097, 64)

# Qubit calculations
control_qubits = 2 * bit_lengths
target_qubits = bit_lengths
total_qubits = control_qubits + target_qubits

# Hardware limit example: IBM Sherbrooke
hardware_limit = 127

# Plot
plt.figure(figsize=(12, 7))

plt.plot(bit_lengths, total_qubits, label="Total Qubits (Control + Target)", color='blue', marker='o')
plt.plot(bit_lengths, control_qubits, label="Control Qubits (2n)", linestyle='--', color='green', marker='s')
plt.plot(bit_lengths, target_qubits, label="Target Qubits (n)", linestyle='--', color='orange', marker='^')

plt.axhline(hardware_limit, color='red', linestyle='-.', linewidth=2, label="IBM Sherbrooke Qubit Limit (127)")

# Labels and styling
plt.title("Qubits vs. Bit Length of N in Shor's Algorithm")
plt.xlabel("Bit Length of N")
plt.ylabel("Number of Qubits Required")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
