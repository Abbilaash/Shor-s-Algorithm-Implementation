import cv2
import numpy as np
from Crypto.Hash import SHA256
from sympy import nextprime
from math import gcd
import matplotlib.pyplot as plt

# Step 1: Load and preprocess fingerprint image
def preprocess_fingerprint(path):
    original = cv2.imread(path)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

    resized = cv2.resize(gray, (128, 128))
    _, binary = cv2.threshold(resized, 127, 255, cv2.THRESH_BINARY)

    # Show all stages
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 4, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.title("Grayscale")
    plt.imshow(gray, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.title("Resized")
    plt.imshow(resized, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.title("Binarized")
    plt.imshow(binary, cmap='gray')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return binary

# Step 2: Extract fingerprint features and hash to seed
def extract_fingerprint_seed(image):
    block_means = []
    block_size = 16
    vis = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    print("\n📦 Mean values per 16x16 block:")
    for i in range(0, image.shape[0], block_size):
        for j in range(0, image.shape[1], block_size):
            block = image[i:i+block_size, j:j+block_size]
            mean_val = int(np.mean(block))
            block_means.append(mean_val)

            # Draw block mean on visualization image
            cv2.rectangle(vis, (j, i), (j+block_size, i+block_size), (0, 255, 0), 1)
            cv2.putText(vis, str(mean_val), (j+2, i+12), cv2.FONT_HERSHEY_PLAIN, 0.6, (255, 0, 0), 1)

    feature_string = ''.join(map(str, block_means))
    digest = SHA256.new(feature_string.encode()).digest()
    seed_int = int.from_bytes(digest, 'big')

    # Show block-wise mean image
    plt.figure(figsize=(6, 6))
    plt.title("Block Mean Overlay (16x16)")
    plt.imshow(vis)
    plt.axis('off')
    plt.show()

    print(f"\n🧬 Feature String:\n{feature_string[:300]}...")  # show prefix
    print(f"\n🔐 SHA256 Digest (hex): {digest.hex()}")
    print(f"\n🔑 Seed Integer: {seed_int}\n")

    return seed_int

# Step 3: Generate small primes from seed and compute RSA key manually
def generate_small_rsa_key(seed, e=17):
    max_attempts = 100
    attempt = 0

    while attempt < max_attempts:
        p = nextprime(seed % 1000 + attempt)
        q = nextprime((seed // 1000) % 1000 + attempt)
        if p == q:
            q = nextprime(q + 1)

        n = p * q
        phi = (p - 1) * (q - 1)

        if gcd(e, phi) == 1:
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
image_path = "2.png"  # Replace with your actual fingerprint image path
img = preprocess_fingerprint(image_path)
seed = extract_fingerprint_seed(img)
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