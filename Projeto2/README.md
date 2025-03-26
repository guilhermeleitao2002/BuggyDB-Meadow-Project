# Prado Ecosystem Simulator

This project simulates an ecosystem within a meadow (prado) where predators and prey interact, move, feed, reproduce, and die over successive generations. The implementation involves defining abstract data types (ADTs) to model positions, animals, and the meadow, along with functions to manage the simulation rules.

## Abstract Data Types (ADTs)

### 1. **TAD `posicao` (Position)**
Represents a coordinate (x, y) in the meadow.
- **Operations**:
  - `cria_posicao(x, y)`: Creates a valid position (x ≥ 0, y ≥ 0). Raises `ValueError` for invalid inputs.
  - `obter_pos_x(p)`, `obter_pos_y(p)`: Return x and y components of a position.
  - `obter_posicoes_adjacentes(p)`: Returns adjacent positions in clockwise order (up, right, down, left).
  - `ordenar_posicoes(t)`: Sorts positions by reading order (left-to-right, top-to-bottom).

### 2. **TAD `animal` (Animal)**
Models predators and prey with species-specific attributes.
- **Operations**:
  - `cria_animal(s, r, a)`: Creates an animal with species `s`, reproduction frequency `r`, and feeding frequency `a` (0 for prey).
  - `aumenta_idade(a)`, `reset_idade(a)`: Modify age for reproduction.
  - `aumenta_fome(a)`, `reset_fome(a)`: Manage hunger for predators.
  - `eh_animal_fertil(a)`, `eh_animal_faminto(a)`: Check reproduction readiness or starvation.
  - `reproduz_animal(a)`: Creates a new offspring and resets the parent's age.

### 3. **TAD `prado` (Meadow)**
Represents the meadow's layout, obstacles, and animal positions.
- **Operations**:
  - `cria_prado(d, r, a, p)`: Initializes the meadow with dimensions `d`, rocks `r`, animals `a`, and their positions `p`.
  - `obter_posicao_animais(m)`: Returns positions of animals in reading order.
  - `obter_movimento(m, p)`: Determines the next position for an animal based on movement rules.
  - `eliminar_animal(m, p)`, `mover_animal(m, p1, p2)`, `inserir_animal(m, a, p)`: Modify the meadow state.
  - `prado_para_str(m)`: Generates a string representation of the meadow.

## Simulation Rules

### Movement
- **Predators** prioritize moving to adjacent cells with prey. If none, move to an empty cell.
- **Prey** move to empty adjacent cells.
- Movement direction is chosen using the formula `N mod p`, where `N` is the current position's numeric value and `p` is the number of valid adjacent positions.

### Reproduction
- Animals reproduce if their age matches their reproduction frequency. The parent moves, leaving an offspring at the original position.

### Feeding and Death
- Predators reset hunger when eating prey. They die if hunger reaches their feeding frequency.
- Prey die only when eaten.

## Key Functions

### `geracao(m)`
Simulates one generation:
1. Increments age and hunger for all animals.
2. Processes each animal's turn in reading order:
   - Moves, eats, reproduces, or dies based on rules.
3. Returns the updated meadow.

### `simula_ecossistema(f, g, v)`
Runs the simulation for `g` generations using configuration file `f`:
- **File format**: Specifies meadow dimensions, rocks, and initial animals.
- **Verbose mode (`v=True`)**: Outputs the meadow state after each generation if population changes.

## Example Usage
```python
# Sample simulation with 200 generations (quiet mode)
simula_ecossistema('config.txt', 200, False)

# Output includes final predator/prey counts and meadow state:
# Predadores: 0 vs Presas: 28 (Gen. 200)
# (0, 28)
```

## Implementation Notes
- **ADT Integrity**: Functions respect abstraction barriers; only constructors validate inputs.
- **Destructive Modifications**: Functions like `mover_animal` modify the meadow in-place.
- **Efficiency**: Movement and reproduction logic optimizes for sequential processing in reading order.
