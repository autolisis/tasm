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

1. Accept

```assembly
acc

```

2. Reject

```assembly
rej
```

3. Right/Left, moves the head of the TM to the Right/Left

```
right
```

```
left
```

4. Goto `label`

```
goto divCheck
```

5. If Reading `symbol`, go to `label`

```
ifr '0' read0
```
