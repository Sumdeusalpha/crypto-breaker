import secrets

# Core EC functions
def inv_mod(k, p):
    return pow(k, -1, p)

def ec_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and (y1 != y2 or y1 == 0): return None
    if P == Q:
        m = (3 * x1 * x1 + a) * inv_mod(2 * y1, p) % p
    else:
        m = (y2 - y1) * inv_mod(x2 - x1, p) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def ec_mult(k, P, a, p):
    R, Q = None, P
    while k:
        if k & 1:
            R = ec_add(R, Q, a, p)
        Q = ec_add(Q, Q, a, p)
        k >>= 1
    return R

# Distance metrics
def hamming_distance_coords(P, Q):
    return bin(P[0] ^ Q[0]).count('1') + bin(P[1] ^ Q[1]).count('1')

def coordinate_distance(Q1, Q2):
    return ((Q1[0] - Q2[0]) ** 2 + (Q1[1] - Q2[1]) ** 2) % prime

# Symbolic scoring
def symbolic_score(scalar, dist):
    grad_phi = 1 / (dist + 1e-6)
    curvature_resistance = (scalar % 13) + 1
    return grad_phi / curvature_resistance

# Collapse convergence engine
class CollapseConvergenceEngine:
    def __init__(self, G, Q_target, a, p, curve_order):
        self.G = G
        self.Q_target = Q_target
        self.a = a
        self.p = p
        self.curve_order = curve_order
        self.history = []
        self.best = None

    def validate_scalar(self, scalar):
        Q = ec_mult(scalar, self.G, self.a, self.p)
        if Q is None: return None
        match = Q[0] == self.Q_target[0] and (Q[1] == self.Q_target[1] or Q[1] == (-self.Q_target[1] % self.p))
        dist = 0 if match else hamming_distance_coords(Q, self.Q_target)
        coord_dist = coordinate_distance(Q, self.Q_target)
        score = symbolic_score(scalar, dist)
        result = {
            'scalar': scalar,
            'Q': Q,
            'dist': dist,
            'coord_distance': coord_dist,
            'score': score
        }
        self.history.append(result)
        if self.best is None or dist < self.best['dist']:
            self.best = result
        return result

    def sweep_resonance_basin(self, center_scalar, sweep_range=100000, step=1):
        for offset in range(-sweep_range, sweep_range + 1, step):
            scalar = (center_scalar + offset) % self.curve_order
            result = self.validate_scalar(scalar)
            if result and result['dist'] == 0:
                print(f"[CONVERGENCE SUCCESS] Scalar {scalar} matches target.")
                return result
        return self.best
