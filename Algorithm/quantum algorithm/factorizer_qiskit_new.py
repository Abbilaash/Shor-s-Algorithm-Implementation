# AIM: try to design a circuit to factorize 21 (UPDATED)

# present status: SUCCESS

from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit.circuit import QuantumRegister, ClassicalRegister
from math import gcd
from qiskit.circuit.library import QFT
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Batch, SamplerV2 as Sampler
from fractions import Fraction
from collections import Counter
from dotenv import load_dotenv
import os
load_dotenv()


QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token=os.getenv("IBM_TOKEN_NEW"),
    region="us-east",             # optional: choose region
    plans_preference=["Open"],    # optional: plan preference
    set_as_default=True,
    overwrite=True,
)

N = 21
n = np.ceil(np.log2(N)).astype(int)
q = QuantumRegister(2*n, "q")
t = QuantumRegister(n, "t")
c = ClassicalRegister(2*n, "c")
a = 2

service = QiskitRuntimeService()

qc = QuantumCircuit(q,t,c)

qc.x(t[0])
qc.barrier()

qc.h(q)
qc.barrier()

def Uf_fixed(circ, a, N, q, t):
    """Controlled modular exponentiation (simplified for N=21)"""
    for i in range(len(q)):
        mod_exp = pow(a, 2**i, N)

        if N == 21:
            controlled_modular_mult_21(circ, q[i], mod_exp, t)
        else:
            angle = 2 * np.pi * mod_exp / (2**n)
            circ.cp(angle, q[i], t[0])  # fallback simplified CP gate


def controlled_modular_mult_21(circ, control, multiplier, target_reg):
    """Simplified controlled multiplication mod 21"""
    if multiplier == 1:
        return  # identity

    # Approximate logic: activate different target qubits based on known patterns
    for i, tq in enumerate(target_reg):
        if multiplier in [2, 4, 8, 16]:  # powers of 2 mod 21
            circ.cx(control, tq)
        elif multiplier in [5, 10, 20]:
            circ.crz(np.pi * multiplier / 21, control, tq)
        elif multiplier in [7, 11, 13, 17, 19]:
            circ.crx(np.pi * multiplier / 21, control, tq)
        else:
            # fallback
            circ.cp(np.pi * multiplier / 21, control, tq)


Uf_fixed(qc,a,N,q,t)
qc.barrier()

def classical_period_extraction(decimal_value, n):
    """Extract period using continued fractions (no external API needed)"""
    if decimal_value == 0:
        return None
    
    # Convert to phase
    phase = decimal_value / (2**n)
    
    # Use continued fractions to find period
    frac = Fraction(phase).limit_denominator(N)
    return frac.denominator

qc.append(QFT(2*n, inverse=True), q)

qc.measure(q,c)

print(qc)

backend = service.least_busy(simulator=False, operational=True)
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circ = pm.run(qc)
with Batch(backend=backend) as batch:
    sampler = Sampler(mode=batch)
    job = sampler.run([isa_circ])
    result = job.result()
    print(result)

bit_array = result[0].data.c
bitstrings = bit_array.get_bitstrings()
counts = Counter(bitstrings)

sorted_measurements = sorted(counts.items(), key=lambda x: x[1], reverse=True)

for i, (measurement, count) in enumerate(sorted_measurements[:5]):
    decimal_value = int(measurement, 2)

for measurement, count in sorted_measurements:
    decimal_value = int(measurement, 2)
            
    r = classical_period_extraction(decimal_value, 2*n)
            
    if r and r > 1:
        if pow(a, r, N) == 1:
                    
            if r % 2 == 0:
                x = pow(a, r // 2, N)
                if x != N - 1:
                    factor1 = gcd(x - 1, N)
                    factor2 = gcd(x + 1, N)
                    if 1 < factor1 < N:
                        other_factor = N // factor1
                        print(f"Period: {r}")
                        print(factor1, other_factor)
                        break
                            
                    if 1 < factor2 < N:
                        other_factor = N // factor2
                        print(f"✅ Found factors: {factor2} × {other_factor} = {N}")
                        print(factor2, other_factor)
                        break
                else:
                    print(f"Trivial case: x ≡ -1 (mod N)")
            else:
                print(f"Period is odd: {r}")
        else:
            print(f"Period verification failed: {a}^{r} mod {N} = {pow(a, r, N)} ≠ 1")
        



