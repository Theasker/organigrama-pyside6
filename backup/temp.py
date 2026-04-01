usuarios = [("Ana", 25), ("Juan", 19), ("Zoe", 32)]

usuarios.sort(key=lambda x: x[0], reverse=True)
print(usuarios)
print(type(usuarios[0]))