from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from math import gcd
import numpy as np




def apply_controlled_modular_exponentiation(qc, a, N, n_qubits, ctrl_start, tgt_start):
    """Apply controlled modular multiplication gates for a^2^k mod N."""
    exponents = [pow(a, 2 ** i, N) for i in range(n_qubits)]
    for i, exp in enumerate(exponents):
        label = f"{a}^{2**i} mod {N}"
        # For small N, we just label the action (placeholder for real modular multiplication)
        # This assumes the second register has 2*n_qubits - n_qubits = n_qubits size
        ctrl = ctrl_start + i
        tgt_qubits = list(range(tgt_start, tgt_start + n_qubits))
        dummy_gate = QuantumCircuit(n_qubits).to_gate(label=label)
        dummy_gate = dummy_gate.control(1)
        qc.append(dummy_gate, [ctrl] + tgt_qubits)


def quantum_period_finding(N, a):
    if gcd(a, N) != 1:
        print(f"Classical GCD found: {gcd(a, N)} and {N // gcd(a, N)}")
        return None

    print(f"Quantum period finding for N={N}, a={a}")

    # Number of qubits (adjust based on N)
    n_qubits = 2  # Enough to represent N=21 (log2(21) ≈ 5, but simplified)
    qc = QuantumCircuit(2 * n_qubits, n_qubits)

    # Initialize |1> in the second register
    qc.x(2 * n_qubits - 1)

    # Apply Hadamard gates to the first register
    for qubit in range(n_qubits):
        qc.h(qubit)

    # Simplified modular exponentiation (for a=2, N=21)
    # Replace with controlled-U gates for general 'a'
    apply_controlled_modular_exponentiation(qc, a, N, n_qubits, ctrl_start=0, tgt_start=n_qubits)

    # Inverse QFT to extract period
    qc.append(QuantumCircuit(n_qubits).inverse().to_gate(label="QFT†"), range(n_qubits))

    # Measure the first register
    qc.measure(range(n_qubits), range(n_qubits))

    print(qc)

    # Simulate
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled).result()
    counts = result.get_counts()

    # Return the most likely measured phase (simplified)
    measured_phase = int(max(counts, key=counts.get), 2)
    return measured_phase

# Classical post-processing to find factors from 'r'
def classical_post_processing(N, a, measured_phase):
    print(f"Measured phase: {measured_phase}")

    # Estimate period 'r' (simplified; use continued fractions for full impl.)
    r = measured_phase  

    # Check if 'r' is even and non-trivial
    if r % 2 != 0:
        print(f"Period r={r} is odd. Retry with another 'a'.")
        return None

    x = (a ** (r // 2)) % N
    if x == N - 1:
        print(f"Trivial solution (x ≡ -1 mod N). Retry.")
        return None

    p = gcd(x + 1, N)
    q = gcd(x - 1, N)

    if p == 1 or q == 1:
        print(f"Trivial factors (1 and {N}). Retry.")
        return None

    print(f"Non-trivial factors of {N}: {p} and {q}")
    return (p, q)

# Example usage
N = 21
a = 2

# Quantum part: Find period
measured_phase = quantum_period_finding(N, a)

# Classical part: Compute factors
if measured_phase is not None:
    factors = classical_post_processing(N, a, measured_phase)
    print(f"Prime factors of {N}: {factors}")