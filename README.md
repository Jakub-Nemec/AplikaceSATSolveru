# Intersection Number Solver (SAT Reduction)

## Popis projektu
Tento projekt implementuje řešení problému Intersection Number grafu pomocí SAT solveru Glucose. Intersection Number je minimální počet intervalů, které lze přiřadit vrcholům grafu tak, aby každá hrana odpovídala průniku alespoň jednoho intervalu obou vrcholů.

Projekt obsahuje Python skript `script.py`, který:
- Přijímá vstupní graf.
- Generuje CNF formuli ve formátu DIMACS.
- Spouští SAT solver Glucose.
- Dekóduje výsledek a vypisuje přiřazení intervalů pro jednotlivé vrcholy.

---

