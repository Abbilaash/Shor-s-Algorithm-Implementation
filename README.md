# A Quantum Framework for Cryptographic Attacks on Fingerprint Based Authentication

## Litaerture Overview
-  Two-Factor-Based RSA Key Generation from Fingerprint Biometrics and Password
RSA key pair is derived using fingerprint minutiae + password.
Eliminates need to store private key by regenerating it dynamically.
Public key is shared, private key is computed when needed.
Citation: _Asad, M., Alam, M. S., & Razaque, A. (2022). Two-factor-based RSA key generation from fingerprint biometrics and password for secure communication. SN Computer Science, 3, 388._
-  RSA Cryptography-Based Multi-Modal Biometric Identification System
RSA is used to encrypt combined biometric templates (e.g., fingerprint + face).
Focuses on feature-level fusion and RSA-based encryption of the biometric vector.
Shows better template security but depends on classical RSA security.
Source: _Iyer, A., & Jayapriya, S. (2019). RSA Cryptography based Multi-Modal Biometric Identification System for Enhanced Security. International Journal of Electrical and Computer Engineering (IJECE), 9(2), 960–967._
- Cryptography Based on Fingerprint Biometrics
Proposes using fingerprint features directly as entropy for encrypting messages.
Reinforces real-world use of RSA and public-key cryptography in biometric data protection.
Source: _Harish, G., & Vijayalakshmi, D. (2024). Cryptography based on Fingerprint Bio Metrics. Published on ResearchGate._

## Why it matters?
- Operating crypto systems might remain secure today, but quantum advances mean encrypted biometric data must be resilient for decades.
- This research provides a tangible baseline, showcasing how soon-to-be-available quantum algorithms could threaten current biometric encryption practices.

## Workflow
- Simulate a complete fingerprint-based RSA encryption pipeline.
    - Study of the RSA encryption mechanism, its known vulnerabilities, and its real-world implications in biometric security systems.
- Encrypt biometric templates using RSA (public key).
- Apply Quantum Factoring algorithms on the public key to retrieve the private key.
    - Apply concepts like quantum information theory, modulo exponentiation, Inverse Quantum Fourier transform
- Use recovered private key to decrypt the fingerprint template.

## Formalized Problem Statement
Can RSA-based biometric encryption systems, even those using dynamic key generation from fingerprint templates, be compromised using quantum period-finding algorithms such as Shor’s, and how can such systems be made post-quantum secure?

## Future Extensions
- Expand the study on vulnerabilities of multi-modal biometric systems (face + fingerprint + retinal)
- Replace RSA with post quantum cryptography methods like Crytals Kyber and test the vulnerability (lattice-based encryption)
- Scale shor’s factoring algorithm with practical and in real encryption keys

## Resource Metrics
<img width="1489" height="730" alt="image" src="https://github.com/user-attachments/assets/5bda231e-ba46-474f-b509-fbd32b25b426" />

## Contact
A T Abbilaash - 23n201@psgtech.ac.in

