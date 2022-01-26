class Vector:
    def __init__(self, a: list):
        self.v = a

    def __str__(self):
        return "\n".join(map(str, self.v))

    def __iter__(self):
        return iter(self.v)


class Matrix:
    def __init__(self, a: list or tuple, atype: type = int):
        self.type = atype
        if isinstance(a, list):
            self.n = len(a)
            self.m = len(a[0])
            self.mat = [v.copy() for v in a]
        else:
            self.n = a[0]
            self.m = a[1]
            x = atype(0)
            self.mat = [[x] * self.m for _ in range(self.n)]

    def add_vector(self, vec: Vector) -> None:
        """ベクトルを後ろに付け加える"""
        for v, w in zip(self.mat, vec):
            v.append(w)

    def change(self, s: int, t: int) -> None:
        """行の交換"""
        self.mat[s], self.mat[t] = self.mat[t], self.mat[s]

    def rank(self) -> int:
        k = 0
        for i in range(self.n):
            mx = self.type(0)
            while k < self.m:
                mx = abs(self.mat[i][k])
                idx = i
                for j in range(i, self.n):
                    if mx < abs(self.mat[j][k]):
                        mx = abs(self.mat[j][k])
                        idx = j
                if mx == self.type(0):
                    k += 1
                    continue

                self.change(i, idx)
                mx = self.mat[i][k]
                for j in range(k, self.m):
                    self.mat[i][j] /= mx
                for j in range(i + 1, self.n):
                    p = self.mat[j][k]
                    for l in range(k, self.m):
                        self.mat[j][l] -= p * self.mat[i][l]
                break
            if k == self.m:
                return i
        return self.n

    def is_independent_set(self) -> bool:
        return self.rank() == self.m

    def choice(self, *args):
        """args列のvectorのmatrixを返す"""
        res = [[] for _ in range(self.n)]
        for i in range(self.n):
            for j in args:
                res[i].append(self.mat[i][j])
        return Matrix(res, self.type)

    def __str__(self):
        return "\n".join([" ".join(map(str, v)) for v in self.mat])
