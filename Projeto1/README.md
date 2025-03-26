# Buggy Data Base (BDB)

## Overview
This project involves developing a Python program to identify and correct problems in a corrupted database (Buggy Data Base, BDB) that incorrectly refuses access to registered users. The project is divided into five independent tasks:

## Tasks

### 1. Documentation Correction
- Correct corrupted text by:
  - Removing adjacent uppercase/lowercase letter pairs
  - Eliminating anagrams from the text
- Functions developed:
  - `corrigir_palavra()`: Corrects individual words
  - `eh_anagrama()`: Checks if two words are anagrams
  - `corrigir_doc()`: Corrects entire document

### 2. PIN Discovery
- Decode a PIN based on a sequence of keyboard movements
- Movement rules:
  - Start at button '5'
  - Move using 'C' (up), 'B' (down), 'E' (left), 'D' (right)
- Functions developed:
  - `obter_posicao()`: Calculates new position after a movement
  - `obter_digito()`: Determines digit after a sequence of movements
  - `obter_pin()`: Generates PIN from movement sequence

### 3. Data Consistency Verification
- Validate database entries
- Check if control sequence matches encrypted text
- Functions developed:
  - `eh_entrada()`: Checks if an entry is valid
  - `validar_cifra()`: Validates entry's control sequence
  - `filtrar_bdb()`: Filters out inconsistent entries

### 4. Data Decryption
- Decrypt database entries
- Decrypt using a security number and character position
- Functions developed:
  - `obter_num_seguranca()`: Calculates security number
  - `decifrar_texto()`: Decrypts text
  - `decifrar_bdb()`: Decrypts entire database

### 5. Password Debugging
- Validate user passwords
- Check against general and individual password rules
- General rules:
  - At least three lowercase vowels
  - At least one character appearing twice consecutively
- Individual rules specify minimum and maximum occurrences of a specific character
- Functions developed:
  - `eh_utilizador()`: Validates user entry
  - `eh_senha_valida()`: Checks password validity
  - `filtrar_senhas()`: Filters out invalid passwords

## Project Goals
- Develop modular Python functions
- Handle text manipulation
- Implement complex decryption and validation algorithms
- Practice error handling and input validation

## Technologies
- Python 3
- String manipulation
- Algorithm design
- Error handling

## Skills Demonstrated
- Text processing
- Cryptography basics
- Algorithmic problem-solving
- Function design and implementation
