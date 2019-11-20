# TASM

An assembly language for Turing Machines.

## **_ This repository is a work in progress _**

This project aims to write a simple assembler which outputs the state transition table for a Turing machine given TASM code.

## TASM consists of the following constructs

### Comments

```assembly
# This is a comment
```

### Labels

```asm
label:
```

### Instructions

1. Accept (Instantly accepts)

```assembly
acc

```

2. Reject (Instantly rejects)

```assembly
rej
```

3. Right (Moves the head of the TM to the Right)

```assembly
right
```

4. Left (Moves the head of the TM to the Left)

```assembly
left
```

5. Goto `label` (Starts executing from the label)

```assembly
goto divCheck
```

6. If Reading `symbol`, go to `label` (Starts executing from the label if the head points to the symbol)

```assembly
ifr '0' read0
```
