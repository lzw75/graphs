# -----------------------------------------------------
# This program computes the number of simple graphs
# with n vertices, up to isomorphism. 
# See https://oeis.org/A000088
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
    total = 0

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

        power_2 = 0
        for x in part:
            power_2 += x // 2

        for i in range(len(part)):
            x = part[i]
            for y in part[i+1:]:
                power_2 += gcd(x, y)

        total += (2 ** power_2) * num

    div = fact(n)
    assert total % div == 0
    return total // div


for n in range(1, 21):
    print(n, compute_graphs(n))
