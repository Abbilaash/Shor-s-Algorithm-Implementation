from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
from qiskit.circuit.library import QFT
from math import gcd
import numpy as np
from math import pi

QiskitRuntimeService.save_account(channel='ibm_quantum',token='73400f3fc9487c07ea601ce35f3c6a1dd052fe253283f8afced43eb1e1ce4e12852c8a281639229d84a6ffdd16034e30dda16dd7f42e0799373860910190bce1',overwrite=True)
service = QiskitRuntimeService()



def apply_controlled_modular_exponentiation(qc, a, N, n_qubits, ctrl_start, tgt_start):
    """Apply controlled modular multiplication gates for a^2^k mod N."""
    exponents = [pow(a, 2 ** i, N) for i in range(n_qubits)]
    for i, exp in enumerate(exponents):
        label = f"{a}^{2**i} mod {N}"
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
    n_qubits = 2
    qreg_q = QuantumRegister(2 * n_qubits, name="q")
    cr = ClassicalRegister(n_qubits*2*2, name="c")
    qc = QuantumCircuit(qreg_q, cr)

    # Initialize |1> in the second register
    qc.x(qreg_q[2 * n_qubits - 1])

    # Apply Hadamard gates to the first register
    for qubit in range(n_qubits):
        qc.h(qreg_q[qubit])

    # Apply controlled modular exponentiation
    #apply_controlled_modular_exponentiation(qc, a, N, n_qubits, ctrl_start=0, tgt_start=n_qubits)
    qc.cx(qreg_q[3], qreg_q[2])
    qc.cx(qreg_q[0], qreg_q[3])
    qc.ccx(qreg_q[0],qreg_q[2],qreg_q[3])

    # Inverse QFT to extract period
    # qc.append(QuantumCircuit(n_qubits).inverse(annotated=False).to_gate(label="IQFT"), range(n_qubits))
    qc.append(QFT(2, inverse=True, do_swaps=True).to_gate(),[qreg_q[0],qreg_q[1]])


    # Measure the first register
    qc.measure(range(n_qubits), range(n_qubits))

    print(qc)

    backend = service.least_busy(operational=True, simulator=False)
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(qc)

    with Session(backend=backend) as session:
        sampler = Sampler(mode=session)
        job = sampler.run([isa_circuit])
        pub_result = job.result()[0]

        print(f"Sampler job ID: {job.job_id()}")

    print(pub_result)
        
    measured_phase = int(max(pub_result.data.c.get_counts(), key=pub_result.data.c.get_counts().get), 2)
    return measured_phase


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

N = 21
a = 2

# Quantum part: Find period
measured_phase = quantum_period_finding(N, a)

if measured_phase is not None:
    factors = classical_post_processing(N, a, measured_phase)
    print(f"Prime factors of {N}: {factors}")
