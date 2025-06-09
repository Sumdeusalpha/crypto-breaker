# crypto-breaker
Symbolic Entropy Collapse: Scalar Field Folding and Full Key Collapse on 21-bit ECC

# RAITCollapse-21bit

### Symbolic Collapse Engine Submission — Q-Day Prize

This repo contains full reproducible code demonstrating scalar collapse convergence on custom 21-bit ECC field via Symbolic Entropy Collapse (SEC) methods.

## Curve Parameters

- Prime field: p = 1048783
- Curve: y² ≡ x³ + 7 (mod p)
- Generator: G = (231634, 106125)
- Target Q: (1047961, 428633)
- True private scalar d = 653735 (recovered)

## Execution

```bash
pip install jupyter
jupyter notebook

