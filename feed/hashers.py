from django.contrib.auth.hashers import BasePasswordHasher

class TextoLimpoHasher(BasePasswordHasher):
    algorithm = "plaintext"

    def encode(self, password, salt):
        # Em vez de embaralhar, apenas retorna a senha como ela é
        return f"{self.algorithm}$$$" + password

    def verify(self, password, encoded):
        # Para verificar, apenas checa se a senha bate com a parte salva
        algo, _, _, hash_val = encoded.split('$', 3)
        return password == hash_val

    def safe_summary(self, encoded):
        return {'algorithm': self.algorithm}
