import cv2
import numpy as np
from Crypto.Hash import SHA256
from sympy import nextprime
from math import gcd

# Step 1: Load and preprocess fingerprint image
def preprocess_fingerprint(path):
    img = cv2.imread(path, 0)
    img = cv2.resize(img, (128, 128))
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return binary

# Step 2: Extract fingerprint features and hash to seed
def extract_fingerprint_seed(image):
    block_means = [int(np.mean(image[i:i+16, j:j+16]))
                   for i in range(0, image.shape[0], 16)
                   for j in range(0, image.shape[1], 16)]
    feature_string = ''.join(map(str, block_means))
    digest = SHA256.new(feature_string.encode()).digest()
    return int.from_bytes(digest, 'big')

# Step 3: Generate small primes from seed and compute RSA key manually
def generate_small_rsa_key(seed, e=17):
    max_attempts = 100
    attempt = 0

    while attempt < max_attempts:
        # Get candidate primes
        p = nextprime(seed % 1000 + attempt)
        q = nextprime((seed // 1000) % 1000 + attempt)
        if p == q:
            q = nextprime(q + 1)

        n = p * q
        phi = (p - 1) * (q - 1)

        if gcd(e, phi) == 1:
            # Compute modular inverse
            def modinv(a, m):
                for d in range(1, m):
                    if (a * d) % m == 1:
                        return d
                return None

            d = modinv(e, phi)
            return {
                "p": p, "q": q, "n": n, "phi": phi,
                "e": e, "d": d
            }

        attempt += 1
    
    raise ValueError("Failed to find valid (p, q) pair with gcd(e, phi) = 1")

# === Run pipeline ===
image_path = "1.jpg"
img = preprocess_fingerprint(image_path)
seed = extract_fingerprint_seed(img)
print(f"Seed: {seed}")
rsa = generate_small_rsa_key(seed, e=17)

# Output result
print("🔓 Public Key: ")
print(f"N = {rsa['n']}, e = {rsa['e']}")
print("🔐 Private Key:")
print(f"d = {rsa['d']}")
print(f"p = {rsa['p']}, q = {rsa['q']}")


# N = 134041
# p=431 , q=311
# d = 86253