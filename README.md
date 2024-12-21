# Intersection Number Solver  

Tento projekt implementuje řešení problému **Intersection Number** grafu pomocí SAT solveru **Glucose**. Skript generuje CNF formuli ve formátu DIMACS, kterou následně řeší pomocí Glucose a dekóduje výsledky zpět na intervalové přiřazení vrcholům grafu.  

---

## 1. Popis problému: Intersection Number  

Intersection Number grafu \( G = (V, E) \) je definováno jako minimální počet intervalů \( k \), takových že:  
- Každému vrcholu \( v \in V \) je přiřazena množina intervalů \( I_v \subseteq \{1, \ldots, k\} \).  
- Každá hrana \( (u, v) \in E \) má alespoň jeden průnik mezi intervaly \( I_u \) a \( I_v \), tj. \( I_u \cap I_v \neq \emptyset \).  

---

## 2. Zakódování do SAT (CNF formát)  

### Proměnné:  
Každý vrchol \( v \) je reprezentován pomocí proměnných:  
\[
x_{v,k} = 1 \text{ pokud je vrchol } v \text{ přiřazen intervalu } k
\]  
Celkový počet proměnných je \( |V| \times k \).  

### Omezení:  
1. **Pokrytí hran:**  
Každá hrana \( (u, v) \) musí být pokryta alespoň jedním intervalem:  
\[
\bigvee_{k=1}^K (x_{u,k} \land x_{v,k})
\]  

2. **DIMACS CNF formát:**  
- Každá klauzule odpovídá pokrytí jedné hrany pro všechny intervaly.  
- Všechny klauzule jsou zapsány do souboru `problem.cnf`.  

---

## 3. Uživatelská dokumentace  

### Požadavky:  
- **Python 3**  
- SAT solver **Glucose 4.2** (spustitelný soubor `glucose` musí být ve stejné složce jako skript)

---

### Spuštění skriptu:  

python IntersectionNumberSatSolver.py

##Formát vstupu:
Graf je zadán jako slovník:
graph = {
    'vertices': [1, 2, 3],
    'edges': [(1, 2), (2, 3), (3, 1)]
}

- vertices – seznam vrcholů.
- edges – seznam hran grafu jako dvojice vrcholů.
- Počet intervalů se nastavuje proměnnou num_intervals ve skriptu.

### Formát výstupu:
### 1. Splnitelné (SAT):
- Satisfiable: solution found.
- Assignments: {1: [0], 2: [0], 3: [0]}
### 2. Nesplnitelné (UNSAT):
- Unsatisfiable: no solution exists.
- Výstup zobrazuje přiřazení intervalů jednotlivým vrcholům.

## 4. Popis experimentů a přiložené instance
Testovací instance:
Složka instances/ obsahuje tři instance:

#### smallSat.txt:
c Splnitelná instance (K3, k=2)
p cnf 6 3
1 2 0
3 4 0
5 6 0

#### smallUnsat.txt:
c Nesplnitelná instance (K3, k=1)
p cnf 3 3
1 0
2 0
3 0

#### long_running.txt
c Instance s dlouhým během (10 vrcholů, 24 hran, k=3)
p cnf 30 24
1 2 0
3 4 0
5 6 0
7 8 0
9 10 0
11 12 0
13 14 0
15 16 0
17 18 0
19 20 0
21 22 0
23 24 0
25 26 0
27 28 0
29 30 0

#### Experimenty:
- **Cíl**: Najít minimální počet intervalů k, pro který je problém splnitelný.
**Postup**:
- Testujeme hodnoty k od 1 směrem nahoru.
- Pro každé k generujeme CNF a spustíme Glucose.
- První splnitelné k je řešení Intersection Number.

## 5. Výsledky experimentů:
Výsledky jsou uloženy ve složce results/:

- smallSatSolution.txt – Řešení pro splnitelnou instanci.
- smallUnsatSolution.txt – Výstup SAT solveru pro nesplnitelnou instanci.
- longRunningSolution.txt – Výsledky pro velkou instanci.

#### Poznámky k experimentům:
- **Malé instance (3-5 vrcholů)**: Řešitelné během milisekund.
- **Střední instance (6-15 vrcholů)**: SAT solver běží do 1 sekundy.
- **Velké instance (20+ vrcholů)**: Běh trvá několik sekund až minut v závislosti na počtu hran a intervalů.

## 6. Možné rozšíření:
- Iterativní optimalizace: Skript by mohl automaticky hledat minimální k iterativním spouštěním SAT solveru pro rostoucí k.
- Paralelizace: Paralelní testování různých hodnot k.
- Alternativní CNF kodování: Optimalizace počtu klauzulí a zlepšení výkonu solveru.
