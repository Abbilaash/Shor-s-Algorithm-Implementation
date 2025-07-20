from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit.circuit import QuantumRegister, ClassicalRegister
from math import gcd
from qiskit.circuit.library import QFT, ModularAdderGate
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2 as Sampler
import random
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from fractions import Fraction
import os
from dotenv import load_dotenv
load_dotenv()

# === SETUP ACCOUNT ===
QiskitRuntimeService.save_account(
    channel='ibm_quantum',
    token=os.getenv("IBM_TOKEN_OLD"),
    overwrite=True
)
service = QiskitRuntimeService()

# === PROBLEM ===
N = 134041
n = int(np.ceil(np.log2(N)))
q = QuantumRegister(2 * n, name='q')
t = QuantumRegister(n, name='t')
aux = QuantumRegister(n, name='aux')  # new ancilla register for arithmetic
c = ClassicalRegister(2 * n, name='c')

def classical_period_extraction(decimal_value, n_bits):
    if decimal_value == 0:
        return None
    phase = decimal_value / (2 ** n_bits)
    frac = Fraction(phase).limit_denominator(N)
    return frac.denominator

def controlled_modular_mult(circ, control, multiplier, N, target_reg, aux_reg):
    """Controlled multiply target_reg by multiplier mod N with ModularAdderGate."""
    for i in range(n):
        circ.cx(target_reg[i], aux_reg[i])  # copy

    bits = [(multiplier >> i) & 1 for i in range(n)]
    for i, bit in enumerate(bits):
        if bit:
            shifted = aux_reg[i:] + [q[0]]*(i)  # wrap-around fill
            adder = ModularAdderGate(num_state_qubits=n)
            circ.append(adder.control(1),
                       [control] + list(aux_reg) + list(target_reg))

    for i in range(n):
        circ.cx(target_reg[i], aux_reg[i])  # uncompute

def Uf(circ, a, N, exp_reg, target_reg, aux_reg):
    """Full modular exponentiation using controlled modular multipliers."""
    for i, ctrl in enumerate(exp_reg):
        mult = pow(a, 2**i, N)
        controlled_modular_mult(circ, ctrl, mult, N, target_reg, aux_reg)

def run_shors_algorithm():
    state = False
    while not state:
        a = 2  # or random.randint(2, N-1)
        if gcd(a, N) > 1:
            f = gcd(a, N)
            print(f"Lucky GCD factor: {f} × {N//f}")
            return (f, N//f)

        print(f"Chosen base a = {a}")
        qpe = QuantumCircuit(q, t, aux, c)
        qpe.x(t[0]); qpe.barrier()
        qpe.h(q); qpe.barrier()
        Uf(qpe, a, N, q, t, aux); qpe.barrier()
        qpe.append(QFT(2 * n, inverse=True), q)
        qpe.measure(q, c)

        print(f"Circuit: qubits={qpe.num_qubits}, depth={qpe.depth()}")

        backend = service.least_busy(operational=True, simulator=False)
        print(f"Using backend: {backend}")
        print("[+] Backend fixed !!!")
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        print("[+] Generate pass manager done")
        print("[+] pass manager running started...")
        isa_circ = pm.run(qpe)
        print("[+] Pass manager running done")
        with Session(backend=backend) as session:
            print("[+] Session started")
            sampler = Sampler(mode=session)
            print("[+] Sampler created")
            print("[+] Running sampler...")
            res = sampler.run([isa_circ], shots=1024).result()
            print("[+] Sampler run completed")
            from collections import Counter
            counts = Counter(res[0].data.c.get_bitstrings())
        print(f"Sampler job ID: {res.job_id()}")

        sorted_meas = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        print("Top 5 measurements:")
        for bit, cnt in sorted_meas[:5]:
            print(f"  {bit} → {int(bit,2)}  (shots={cnt})")

        for bit, cnt in sorted_meas:
            dec = int(bit, 2)
            r = classical_period_extraction(dec, 2*n)
            if r and r > 1 and pow(a, r, N) == 1:
                if r % 2 == 0:
                    x = pow(a, r // 2, N)
                    f1, f2 = gcd(x-1, N), gcd(x+1, N)
                    if 1 < f1 < N:
                        print(f"✅ Factors: {f1} × {N//f1}")
                        return (f1, N//f1)
                    if 1 < f2 < N:
                        print(f"✅ Factors: {f2} × {N//f2}")
                        return (f2, N//f2)

        print("No factors this attempt — modify 'a'.")
        break
    return None

if __name__ == "__main__":
    print(f"🌟 Factoring N = {N}")
    result = run_shors_algorithm()
    print(f"Result: {result}")
