# Project Portfolio: BDB & Prado Ecosystem

## 1. Buggy Data Base (BDB)  
A Python-based solution to repair and validate a corrupted database.  

### Key Features:  
- **Document Correction**:  
  - Fix corrupted words by removing adjacent case conflicts (`corrigir_palavra`).  
  - Eliminate anagrams from text (`corrigir_doc`).  
- **PIN Decoding**:  
  - Decode numeric PINs from directional movements (`obter_pin`).  
- **Data Validation**:  
  - Verify entry consistency (`validar_cifra`) and filter invalid data (`filtrar_bdb`).  
- **Decryption**:  
  - Decrypt entries using security numbers (`decifrar_bdb`).  
- **Password Debugging**:  
  - Validate passwords against rules like vowel counts and character repetitions (`filtrar_senhas`).  

---

## 2. Prado Ecosystem Simulator  
A simulation of predator-prey dynamics in a meadow using abstract data types (ADTs).  

### Core Components:  
- **ADTs**:  
  - `posicao`: Models coordinates and adjacency logic.  
  - `animal`: Tracks age, hunger, and reproduction for predators/prey.  
  - `prado`: Manages meadow layout, obstacles, and animal movements.  
- **Simulation Rules**:  
  - **Movement**: Predators target prey; prey seek empty spaces.  
  - **Reproduction**: Animals spawn offspring upon reaching reproduction age.  
  - **Survival**: Predators die from starvation; prey die when eaten.  
- **Key Functions**:  
  - `geracao(m)`: Simulates one generation of ecosystem evolution.  
  - `simula_ecossistema(f, g, v)`: Runs multi-generation simulations from a config file.  

### Example Output:  
```python
simula_ecossistema('config.txt', 200, False)  
# Predadores: 0 vs Presas: 28 (Gen. 200)  
# (0, 28)  
```

## Technologies & Skills  
- **Python 3**: String manipulation, algorithm design, ADT implementation.  
- **Problem-Solving**: Cryptography, data validation, ecosystem modeling.  
- **Key Concepts**: Text processing, simulation logic, abstraction barriers.  
