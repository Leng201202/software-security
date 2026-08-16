from vulnerable_crypto import reset_token
tokens = [reset_token() for _ in range(10)]
for t in tokens:
    print(t)