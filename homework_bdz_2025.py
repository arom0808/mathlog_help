import itertools


def format_literal(lit):
    val = abs(lit)
    row = (val - 1) // 3 + 1
    col = (val - 1) % 3 + 1
    name = f"x{row}{col}"
    return f"¬{name}" if lit < 0 else name


def format_clause(clause):
    if not clause:
        return "⊥"
    return "(" + " ∨ ".join(format_literal(l) for l in sorted(clause, key=abs)) + ")"


def generate_parity_clauses(variables, target_parity):
    clauses = []
    n = len(variables)
    for assignment in itertools.product([0, 1], repeat=n):
        if sum(assignment) % 2 != target_parity:
            clause = []
            for i, val in enumerate(assignment):
                lit = -variables[i] if val == 1 else variables[i]
                clause.append(lit)
            clauses.append(frozenset(clause))
    return clauses


def resolve(c1, c2, pivot):
    res = set(c1) | set(c2)
    res.discard(pivot)
    res.discard(-pivot)
    for lit in res:
        if -lit in res:
            return None
    return frozenset(res)


def main():
    vars_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    cnf = []
    cnf.extend(generate_parity_clauses(vars_matrix[0], 1))
    cnf.extend(generate_parity_clauses(vars_matrix[1], 0))
    cnf.extend(generate_parity_clauses(vars_matrix[2], 0))
    cols = [[vars_matrix[r][c] for r in range(3)] for c in range(3)]
    cnf.extend(generate_parity_clauses(cols[0], 0))
    cnf.extend(generate_parity_clauses(cols[1], 0))
    cnf.extend(generate_parity_clauses(cols[2], 0))
    print("Start:")
    for c in cnf:
        print(f"  {format_clause(c)}")
    current_clauses = set(cnf)
    for pivot in range(1, 10):
        print(f"\nEliminate var {format_literal(pivot)}:")
        pos_clauses = [c for c in current_clauses if pivot in c]
        neg_clauses = [c for c in current_clauses if -pivot in c]
        other_clauses = [c for c in current_clauses if pivot not in c and -pivot not in c]
        new_resolvents = set()
        for c_pos in pos_clauses:
            for c_neg in neg_clauses:
                res = resolve(c_pos, c_neg, pivot)
                if res is not None:
                    new_resolvents.add(res)
        current_clauses = set(other_clauses) | new_resolvents
        for c in new_resolvents.difference(set(other_clauses)):
            print(f"  {format_clause(c)}")
        if frozenset() in current_clauses:
            return


if __name__ == "__main__":
    main()
