from vulnerable_crypto import encrypt_ecb

ct = encrypt_ecb(b"A"*16 + b"A"*16)
blocks = [ct[i:i+16].hex() for i in range(0, len(ct), 16)]
for i, b in enumerate(blocks):
    print(f"block {i}: {b}")
print("block 0 == block 1:", blocks[0] == blocks[1])
