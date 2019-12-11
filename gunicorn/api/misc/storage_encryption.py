import functools
import random


class Algebra:
    def __init__(self):
        pass

    @staticmethod
    def _eval_at(poly, x, prime):
        accum = 0

        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= prime

        return accum

    @staticmethod
    def _extended_gcd(a, b):
        x, last_x = 0, 1
        y, last_y = 1, 0

        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y

        return last_x, last_y

    def _div_mod(self, num, den, p):
        inv, _ = self._extended_gcd(den, p)

        return num * inv

    def _lagrange_interpolate(self, x, x_s, y_s, p):
        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"

        def prod(vals):
            accum = 1
            for v in vals:
                accum *= v
            return accum

        nums = []
        dens = []

        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(prod(x - o for o in others))
            dens.append(prod(cur - o for o in others))

        den = prod(dens)
        num = sum([self._div_mod(nums[i] * den * y_s[i] % p, dens[i], p)
                   for i in range(k)])

        return (self._div_mod(num, den, p) + p) % p


class StorageEncryption(Algebra):

    def __new__(cls, prime=2 ** 127 - 1, minimum=3, n_shares=5):
        instance = super(StorageEncryption, cls).__new__(cls)
        instance.__init__(prime, minimum, n_shares)
        instance.__master_key, shares = instance.__make_random_shares()

        print(f'The new MasterKey was successfully generated according to ({minimum},{n_shares})-threshold spread.')
        return instance, shares

    def __init__(self, prime=2 ** 127 - 1, minimum=3, n_shares=5):
        super(Algebra, self).__init__()
        self.prime = prime
        self.minimum = minimum
        self.n_shares = n_shares
        self.__master_key = None
        self.rand_int = functools.partial(random.SystemRandom().randint, 0)

    def __make_random_shares(self):
        if self.minimum > self.n_shares:
            raise ValueError('pool secret would be irrecoverable')

        poly = [self.rand_int(self.prime) for _ in range(self.minimum)]
        secret, shares = poly[0], [(i, self._eval_at(poly, i, self.prime)) for i in range(1, self.n_shares + 1)]

        return secret, shares

    def recover_secret(self, shares):
        if len(shares) < self.minimum:
            raise ValueError(f'need at least {self.minimum} keys, {len(shares)} given instead')

        x_s, y_s = zip(*shares)

        return self._lagrange_interpolate(0, x_s, y_s, self.prime)

    def rekey(self, shares, minimum, n_shares):
        if self.recover_secret(shares) != self.__master_key:
            raise ValueError("wrong MasterKey")
        else:
            # TODO Request for deleting the old key
            self.minimum = minimum
            self.n_shares = n_shares
            self.__master_key, shares = self.__make_random_shares()
            print(f'MasterKey was successfully regenerated according to ({minimum},{n_shares})-threshold spread.')

            return shares

    def rotate(self):
        x_poly = [self.rand_int(self.prime) for _ in range(self.minimum - 1)]
        shares = [(i, self._eval_at([self.__master_key] + x_poly, i, self.prime)) for i in range(1, self.n_shares + 1)]

        return shares
