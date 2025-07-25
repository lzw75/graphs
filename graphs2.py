# -----------------------------------------------------
# This program computes the number of simple graphs
# with n vertices and t edges, up to isomorphism. 
# Input is n. Output is a list, where the t-th entry
# is the number of such graphs.
# -----------------------------------------------------

# Compute factorial of n.

def fact(n):
    p = 1
    for i in range(1, n+1):
        p *= i
    return p

# Compute P(n, k).

def perm(n, k):
    p = 1
    for i in range(1, k+1):
        p *= n-i+1
    return p 


# Drop leading zeros in a polynomial.

def normalize_p(p):
    while len(p) >= 2 and p[-1] == 0:
        del p[-1]

# Add two polynomials.

def add_pp(p1, p2):
    p = [0] * max(len(p1), len(p2))
    for i in range(len(p1)):
        p[i] = p1[i]
    for i in range(len(p2)):
        p[i] += p2[i]
    normalize_p(p)
    return p

# Multiply two polynomials.

def mul_pp(p1, p2):
    p = [0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            p[i+j] += p1[i] * p2[j]
    normalize_p(p)
    return p

# Multiply scalar by polynomial.

def mul_sp(c, p):
    return mul_pp([c], p)

# Compute (1+x^m)^n.

def pow_1x(m, n):
    p = [0] * (m*n + 1)
    for i in range(n+1):
        p[i*m] = perm(n, i) // fact(i)
    return p


# List all partitions of n, with optional maximum.

def all_partitions(n, maxx=None):
    if maxx == None:
        maxx = n
    curr = []
    if n == 0: return [curr]
    for i in range(1, maxx+1):
        result = all_partitions(n-i, min(i, n-i))
        for part in result:
            curr.append([i] + part)

    return curr

# Assume m, n > 0.

def gcd(m, n):
    while n:
        m, n = n, m % n
    return m


def compute_graphs(n):
    partitions = all_partitions(n)
    total = [0]

    for part in partitions:

        # Compute number of permutations of cycle type.

        num, curr = 1, n
        for x in part:
            num *= perm(curr, x) // x
            curr -= x

        # Need to factor out by repeated cycle lengths.

        curr_len = 1
        for i in range(len(part)-1):
            if part[i] == part[i+1]:
                curr_len += 1
            else:
                num //= fact(curr_len)
                curr_len = 1
        num //= fact(curr_len) # Final result.

#        print(part, num)

        # Compute number of fixed graphs for g.

        count = [1]
        for x in part:
            tmp = pow_1x(x, (x-1)//2)
            if x % 2 == 0:
                tmp = mul_pp(tmp, pow_1x(x//2, 1))
            count = mul_pp(count, tmp)

        for i in range(len(part)):
            x = part[i]
            for y in part[i+1:]:
                z = gcd(x, y)
                count = mul_pp(count, pow_1x(x*y//z, z))

        count = mul_sp(num, count)
        total = add_pp(total, count)

    div = fact(n)
    assert set([x % div == 0 for x in total]) == {True}
    for i in range(len(total)):
        total[i] //= div
    return total


print(compute_graphs(30))
