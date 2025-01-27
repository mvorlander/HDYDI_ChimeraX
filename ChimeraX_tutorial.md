# ChimeraX cheat sheet

## ChimeraX Atom Specification Overview

In ChimeraX, commands often require specifying target items such as atomic models, residues, or atoms. The specification syntax includes:

## Hierarchical Specifiers


Hierarchial specifiers are the most commonly used selection syntax, and include up to four  levels: the *model*, the *chain*, the *residue*, and the *atom* level. 

| Symbol | Reference Level | Definition | Example |
|--------|----------------|------------|---------|
| `#`    | Model           | Model number assigned to data in ChimeraX. Hierarchical with positive integers separated by dots (e.g., N, N.N, N.N.N). | `#1`, `#1.3` |
| `/`    | Chain           | Chain identifier (case-insensitive unless both upper- and lowercase IDs are present). | `/A` |
| `:`    | Residue         | Residue number or name (case-insensitive). | `:51`, `:glu` |
| `@`    | Atom            | Atom name (case-insensitive). | `@ca` |

**Note:** 
If you don't specify a part of the structure, ChimeraX will assume you mean everything at that level.
For example, `#1` means all chains in model 1 if you don't specify a specific chain. `#1:100` matches the one-hundreds residue in all chains of model #1


**Note:** In these examples, we always combine the selection syntax with the `select` command, but it is used in many commands! For example, the `color` command also requires a selection!

---

## Additional Specification Methods

- **Built-in Classifications:**  
  Predefined groups like `protein`, `helix`, `strand`, `ligand`, `solvent`, `hbonds`, element symbols, and functional groups.

- **User-Defined Targets:**  
  Named selections or targets defined with the `name` attribute.

- **Attribute Names and Values:**  
  Specifying items based on their attributes.

- **Zones:**  
  Items within a certain distance from other specified items.

- **Combinations:**  
  Logical combinations of the above methods.

---

## Example Usage

### Select all atoms in model 1:
```
select #1
```

### Select chain B in model 2:
```
select #2/B
```

### Select residue 45 in chain A of model 3:
```
select 3/A:45
```

### Select residues 45-55 in chain A of model 3:
```
#3/A:45-55
```

### Select all lysine residues (LYS) in any model:
```
select :lys
```

### Select the alpha carbon (CA) atoms in model 1, chain A:
```
select #1/A@ca
```
select @ca,n,c,o


### Select lysine residues in chain B only:
```
select #1/B:lys
```

### Select all backbone atoms in a protein:
```
select @ca,n,c,o
```

---

## Logical Combinations

ChimeraX allows logical operators to combine multiple selections:

- **Combining selections with commas (`,`) for OR conditions:**

  Select chain A and B in model 1:
  ```
  select #1/A,B
  ```

  Select residue residues 10 or 20 in all chains of model 1:
  ```
  select #1:10,20
  ```
- **Exlcuding residues from a selection with the `~` operator**
  
  Select everything that is not a nucleic acid:

  ``` 
  select ~ nucleic 
  ```
- **Using `&` (AND) to specify multiple criteria:**

  Select all nucleic acids in model #1
  ```
  select #1 & nucleic
  ```

  Select all residues in model #1 **except** nucleic acids
  ```
  select #1 &~ nucleic
  ```
---

## Distance bases selection  (`select zone`)

The `select zone` command in ChimeraX allows users to select atoms and/or surfaces within a specified distance (cutoff) from reference items.

## **Usage**
```
select zone ref-spec cutoff [other-spec] [extend true|false] [residues true|false]
```

## **Parameters**

- **`ref-spec`**: Reference specification; the atoms and/or surfaces from which the distance is measured.
- **`cutoff`**: The distance cutoff in Ångströms.
- **`other-spec`** *(optional)*: Items to consider for selection within the cutoff distance from `ref-spec`. If omitted, defaults to all items.
- **`extend`** *(optional, default: false)*: If `true`, includes the reference items (`ref-spec`) in the selection.
- **`residues`** *(optional, default: false)*: If `true`, selects entire residues if any of their atoms fall within the zone.

## **Examples**

**Select all protein atoms within 4.5 Å of any ligand**:
```
select zone ligand 4.5 protein
```

**Select all atoms within 8 Å of model #1.2:**
```
select zone #1.2 8
```

**Select all atoms within 8 Å of model #1.2, and include the entire residues that contain an atom within 8 Å:**
```
select zone #1.2 8 residue true
```


**Select all atoms within 5 Å of the current selection and include the reference items (in the example below, residue 50 in chain A of model #1) in the selection:**
```
select zone #1/A:50 5 extend true
```
 
---

For more details, visit the [ChimeraX `select` command documentation](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/select.html#zone).


# Keyboard Selection Shortcuts

- **Up Arrow** – Broaden the selection  
- **Down Arrow** – Narrow the selection  
- **Right Arrow** or **Left Arrow** – Invert the selection within selected models  
- **Shift + Right Arrow** or **Shift + Left Arrow** – Invert the selection within all models  


## Naming selections

The `name` command in ChimeraX assigns a user-defined label to a specific selection or target specification, facilitating easier reference in subsequent commands.

### Usage

```plaintext
name [ frozen ] target-name spec
```

- **`frozen`** (optional): If included, the `target-name` will refer to the exact items specified by `spec` at the time of definition, regardless of future changes.
- **`target-name`**: A user-defined label starting with an alphabetic character, followed by alphanumeric characters, underscores (`_`), plus (`+`), or minus (`-`) signs.
- **`spec`**: The target specification to be labeled.

### Examples

1. **Define a dynamic target for transmembrane residues 34-64 in chain A:**

   ```plaintext
   name tm1 /a:34-64
   ```

   *Usage:*

   ```plaintext
   color tm1 medium blue
   ```

   *Explanation:* The `tm1` target will always refer to residues 34-64 in chain A, even if new models are opened later.

2. **Define a static target for all leucine residues in currently open structures:**

   ```plaintext
   name frozen leus :leu
   ```

   *Usage:*

   ```plaintext
   color leus yellow
   ```

   *Explanation:* The `leus` target will refer only to the leucine residues present at the time of definition.

3. **Define a static target based on the current selection:**

   ```plaintext
   select ligand :<5.5
   ~select solvent
   name frozen pocket sel
   ```

   *Usage:*

   ```plaintext
   color pocket red
   ```

   *Explanation:* The `pocket` target will refer to the atoms within 5.5 Å of any ligand, excluding solvent, as selected at the time of definition.

### Managing User-Defined Targets

- **List all user-defined targets:**

  ```plaintext
  name list
  ```

  *Note:* Including the option `builtins true` will also list built-in targets.

- **Delete a specific user-defined target:**

  ```plaintext
  name delete target-name
  ```

- **Delete all user-defined targets:**

  ```plaintext
  name delete all
  ```

## Additional Information

- User-defined targets are saved within sessions.
- Targets can be automatically defined at ChimeraX startup by including `name` commands in the Startup preferences.

For more detailed information, refer to the [ChimeraX `name` command documentation](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/name.html).


For more details, visit the [ChimeraX Atom Specification documentation](https://www.cgl.ucsf.edu/chimerax/docs/user/commands/atomspec.html).
