import random
import string

"""
Génération de la première clé à l'inscription
"""
def generateUserKey(length: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))