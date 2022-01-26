from linear import Vector, Matrix
from modint import ModInt


def independent_or_dependent(A: Matrix):
    """Aの独立集合と従属を返す"""
    m = A.m
    independent = []   # 独立集合
    dependent = []  # 従属集合
    for bit in range(1 << m):
        choice = []
        for i in range(m):
            if bit >> i & 1:
                choice.append(i)
        B = A.choice(*choice)
        if B.is_independent_set():
            independent.append(tuple(choice))
        else:
            dependent.append(tuple(choice))
    return sorted(independent), sorted(dependent)


def circuit(A: Matrix):
    _, dependent = independent_or_dependent(A)
    dependent = set(dependent)
    res = []
    for s in dependent:
        s = set(s)
        for i in s:
            s.remove(i)
            if tuple(s) in dependent:
                break
            s.add(i)
        else:
            res.append(tuple(sorted(s)))
    return sorted(res)


def is_circuit(circuit: list) -> bool:
    c = [set(v) for v in circuit]
    if len(c) == 0:
        return False
    for u in c:
        for v in c:
            if u != v and (u < v or v < u):
                return False

    for u in c:
        for v in c:
            if u != v:
                u_and_v = u & v
                u_or_v = u | v
                for e in u_and_v:
                    w = u_or_v - {e}
                    for f in c:
                        if f <= w:
                            print(f, w, u, w, e)
                            break
                    else:
                        return False
    return True


def basis(A: Matrix) -> list:
    independent, _ = independent_or_dependent(A)
    idp = set(independent)
    res = []
    for a in independent:
        s = set(a)
        for c in range(A.m):
            if c not in s:
                s.add(c)
                if tuple(sorted(s)) in idp:
                    break
                s.remove(c)
        else:
            res.append(a)
    return res


def all_flat(A: Matrix):
    n = A.n
    m = A.m
    flat = [[] for _ in range(n + 1)]
    for bit in range(1 << m):
        choice = []
        for i in range(m):
            if bit >> i & 1:
                choice.append(i)
        B = A.choice(*choice)
        r = B.rank()
        for i in range(m):
            if not(bit >> i & 1):
                if r + 1 != (A.choice(*(choice + [i]))).rank():
                    break
        else:
            flat[r].append(choice)
    for i in range(n + 1):
        flat[i].sort(key=lambda x: (len(x), x))
    return flat


def view(vec):
    w = sorted(vec, key=lambda x: (len(x), x))
    print(*[list(map(lambda x:x + 1, v)) for v in w], sep="\n")


a = [[1, 0, 0, 1, 1, 0],
     [0, 1, 0, 1, 0, 1],
     [0, 0, 1, 0, 1, 1]]
A = Matrix(a, atype=int)
b = [list(map(ModInt, v)) for v in a]
B = Matrix(b, atype=ModInt)

print("--------------------------")
print("int")
print()
independent, dependent = independent_or_dependent(A)
print("従属集合")
view(dependent)
print()
print("独立集合")
view(independent)
print()
print("サーキット")
c = circuit(A)
view(c)
print()
print("基")
view(basis(A))
print("--------------------------")

print("mod 2")
print()
independent, dependent = independent_or_dependent(B)
print("従属集合")
view(dependent)
print()
print("独立集合")
view(independent)
print()
print("サーキット")
c = circuit(B)
view(c)
print()
print("基")
view(basis(B))
print()
print("flat")
print(*all_flat(B), sep="\n")
print("--------------------------")


print("--------------------------")
c = [[1, 0, 1],
     [0, 1, 1]]

C = Matrix(c, atype=int)
print("test")
print()
independent, dependent = independent_or_dependent(C)
print("従属集合")
view(dependent)
print()
print("独立集合")
view(independent)
print()
print("サーキット")
c = circuit(C)
view(c)
print()
print("基")
view(basis(C))
print()
view(basis(C.choice(0)))
print()
view(basis(C.choice(1, 2)))

print("--------------------------")
