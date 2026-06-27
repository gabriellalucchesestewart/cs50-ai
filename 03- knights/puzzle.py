from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
statement0 = And(AKnight, AKnave)

knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, statement0),
    Implication(AKnave, Not(statement0))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement1 = And(AKnave, BKnave)

knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, statement1),
    Implication(AKnave, Not(statement1))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statementA = Or(
    And(AKnight, BKnight),
    And(AKnave, BKnave)
)

statementB = Or(
    And(AKnight, BKnave),
    And(AKnave, BKnight)
)

knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, statementA),
    Implication(AKnave, Not(statementA)),

    Implication(BKnight, statementB),
    Implication(BKnave, Not(statementB))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # Structure: each character is exactly one of Knight/Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A says either "I am a knight" or "I am a knave" — exactly one of these,
    # and whichever it is, it's only true if A is a knight.
    Or(
        Biconditional(AKnight, AKnight),   # A said "I am a knight"
        Biconditional(AKnight, AKnave)     # A said "I am a knave"
    ),

    # B says "A said 'I am a knave'." — B's statement is true iff B is a knight.
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # B says "C is a knave."
    Biconditional(BKnight, CKnave),

    # C says "A is a knight."
    Biconditional(CKnight, AKnight)
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
