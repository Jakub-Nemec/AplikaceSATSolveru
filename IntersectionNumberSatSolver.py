import subprocess
import sys

def write_dimacs_cnf(graph, num_intervals, filename="problem.cnf"):
    """
    Generuje CNF ve formátu DIMACS pro Intersection Number.
    """
    vertices = graph['vertices']
    edges = graph['edges']
    num_vars = len(vertices) * num_intervals
    clauses = []

    # Každá hrana musí být pokryta alespoň jedním intervalem
    for u, v in edges:
        edge_clause = []
        for k in range(num_intervals):
            edge_clause.append(get_var(u, k, vertices, num_intervals))
            edge_clause.append(get_var(v, k, vertices, num_intervals))
        clauses.append(edge_clause)

    # Zápis do DIMACS CNF souboru
    with open(filename, "w") as f:
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

def get_var(vertex, interval, vertices, num_intervals):
    """
    Vrací index proměnné pro vrchol a interval.
    """
    return vertices.index(vertex) * num_intervals + interval + 1

def run_glucose_solver(cnf_filename="problem.cnf"):
    """
    Spouští Glucose solver a vrací výsledek.
    """
    result = subprocess.run(["/path/to/glucose-4.2.1", cnf_filename], capture_output=True, text=True)
    output = result.stdout
    if "UNSAT" in output:
        return None
    else:
        return parse_solution(output)

def parse_solution(output):
    """
    Dekóduje výstup SAT solveru.
    """
    solution = []
    for line in output.splitlines():
        if line.startswith("v"):
            variables = map(int, line.split()[1:])
            solution.extend(variables)
    return solution

def decode_solution(solution, graph, num_intervals):
    """
    Převádí SAT řešení zpět na přiřazení intervalů.
    """
    vertices = graph['vertices']
    intervals = {v: [] for v in vertices}
    for var in solution:
        if var > 0:
            var -= 1
            vertex = vertices[var // num_intervals]
            interval = var % num_intervals
            intervals[vertex].append(interval)
    return intervals


def load_graph_from_dimacs(filename):
    """
    Načte graf z DIMACS CNF souboru.
    """
    vertices = set()
    edges = []
    num_vars = 0

    with open(filename, "r") as f:
        for line in f:
            # Ignorujeme komentáře
            if line.startswith("c"):
                continue
            # Pokud řádek začíná 'p', čteme počet vrcholů a hran
            elif line.startswith("p"):
                _, _, num_vars, num_edges = line.split()
                num_vars = int(num_vars)
            # Pokud je to hrana (line nezahrnuje komentáře ani záhlaví)
            else:
                vars = list(map(int, line.split()))
                if vars[-1] == 0:
                    vars.pop()  # Odstranění 0 na konci
                u, v = vars[:2]
                edges.append((u, v))
                vertices.update([u, v])

    # Kontrola, že byly nalezeny vrcholy
    if len(vertices) == 0:
        raise ValueError(f"Chyba: Soubor {filename} neobsahuje žádné vrcholy nebo má nesprávný formát.")

    num_intervals = int(num_vars) // len(vertices)
    return {'vertices': list(vertices), 'edges': edges}, num_intervals

def main():
    if len(sys.argv) != 2:
        print("Použití: python IntersectionNumberSatSolver.py <soubor_instance>")
        sys.exit(1)

    instance_file = sys.argv[1]

    # Načtení grafu z DIMACS souboru
    graph, num_intervals = load_graph_from_dimacs(instance_file)

    # Generování CNF a spuštění solveru
    write_dimacs_cnf(graph, num_intervals)
    solution = run_glucose_solver()

    # Zpracování výsledků
    if solution:
        print("Satisfiable: solution found.")
        decoded = decode_solution(solution, graph, num_intervals)
        print("Assignments:", decoded)
    else:
        print("Unsatisfiable: no solution exists.")

if __name__ == "__main__":
    main()
