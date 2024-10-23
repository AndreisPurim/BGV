import math
import random
import numpy as np

def setup(bit_length: int, mod_size: int, base_value: int) -> tuple[int, int, int, int, int]:
    """
    Sets up the key parameters for the cryptographic system.

    Args:
        bit_length (int): Bit length of the message (unused in this version).
        mod_size (int): Size of the modulus in bits.
        base_value (int): Base value for modulus (unused in this version).
        
    Returns:
        tuple: A tuple containing the modulus (q), degree (d), dimension (n), 
               lattice dimension (N), and noise scale (chi).
    """
    q = random.getrandbits(mod_size)
    
    # Hardcoded parameters for simplicity (can be parameterized later)
    q = 10  # Modulus size
    d = 10  # Polynomial degree
    n = 10  # Lattice dimension
    chi = 1  # Noise scale, a simple placeholder

    # Calculate the lattice dimension based on modulus and degree
    N = int(math.ceil((2 * n + 1) * math.log(q, 2)))

    return q, d, n, N, chi

def secret_key_gen(params: tuple[int, int, int, int, int]) -> np.ndarray:
    """
    Generates the secret key for the cryptographic system.

    Args:
        params (tuple): A tuple containing the parameters (q, d, n, N, chi).
        
    Returns:
        np.ndarray: The secret key vector with the first element set to 1.
    """
    q, d, n, N, chi = params
    
    # Random secret key generation in the range [0, q)
    secret_key = np.random.randint(0, q, n + 1)
    
    # First element of the secret key is always set to 1
    secret_key[0] = 1
    
    return secret_key

def public_key_gen(params: tuple[int, int, int, int, int], sk: np.ndarray) -> np.ndarray:
    """
    Generates the public key using the secret key.

    Args:
        params (tuple): A tuple containing the parameters (q, d, n, N, chi).
        sk (np.ndarray): The secret key.
        
    Returns:
        np.ndarray: The public key matrix.
    """
    q, d, n, N, chi = params
    
    # Generate a random matrix A
    A = np.random.randint(0, q, N * n).reshape(N, n)
    
    # Generate random noise vector e
    e = np.random.randint(0, q, N)
    
    # Compute the b vector (b = A * sk[1:] + 2 * e)
    b = np.dot(A, sk[1:]) + 2 * e
    b = b.reshape(N, 1)
    
    # Concatenate b with -A and apply modulus q
    public_key = np.hstack((b, -A)) % q
    
    # Ensure the public key satisfies the equation for correctness
    assert np.all(np.dot(public_key, sk) % q == (2 * e) % q), "Public key generation failed"
    
    return public_key

def encrypt(params: tuple[int, int, int, int, int], pk: np.ndarray, message: int) -> np.ndarray:
    """
    Encrypts a binary message (0 or 1) using the public key.

    Args:
        params (tuple): A tuple containing the parameters (q, d, n, N, chi).
        pk (np.ndarray): The public key.
        message (int): The binary message to encrypt (0 or 1).
        
    Returns:
        np.ndarray: The encrypted ciphertext vector.
    """
    assert message in (0, 1), "Message must be either 0 or 1"
    
    q, d, n, N, chi = params
    
    # Create the message vector (m, 0, 0, ..., 0)
    message_vector = np.array([message] + [0] * n)
    
    # Generate a random binary vector r
    r = np.random.randint(0, 2, N)
    
    # Compute the ciphertext as c = m_vec + pk^T * r
    ciphertext = message_vector + np.dot(pk.T, r)
    
    return ciphertext % q

def decrypt(params: tuple[int, int, int, int, int], sk: np.ndarray, ciphertext: np.ndarray) -> int:
    """
    Decrypts a ciphertext back into the original binary message.

    Args:
        params (tuple): A tuple containing the parameters (q, d, n, N, chi).
        sk (np.ndarray): The secret key.
        ciphertext (np.ndarray): The ciphertext vector.
        
    Returns:
        int: The decrypted message (0 or 1).
    """
    q, d, n, N, chi = params
    
    # Compute the sum of the element-wise product of c and sk, then reduce modulo q
    return (np.sum(ciphertext * sk) % q) % 2

if __name__ == "__main__":
    BIT = 0  # Example message (0 or 1)
    
    # Initialize parameters and keys
    params = setup(1, 1, 1)
    sk = secret_key_gen(params)
    pk = public_key_gen(params, sk)
    
    # Encrypt the message
    ciphertext = encrypt(params, pk, BIT)

    # Output results
    print("Message bit:\t", BIT)
    print("Public key [0]:\t", pk[0])
    print("Public key [1]:\t", pk[1])
    print("Secret key:\t", sk)
    print("Ciphertext:\t", ciphertext)
    print("Decrypted bit:\t", decrypt(params, sk, ciphertext))

