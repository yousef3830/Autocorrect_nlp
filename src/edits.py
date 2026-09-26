def delete_letter(word):
    splits = [(word[:i] , word[i:]) for i in range(len(word))]
    deletes = [L + R[1:] for L,R in splits]
    return deletes


def insert_letter(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    inserts = [L + c + R for L,R in splits for c in letters]
    return inserts


def switch_letters(word):
    splits = [(word[:i],word[i:]) for i in range(len(word))]
    switches = [L[:-1] + R[0] + L[-1] + (R[1:] or "") for L,R in splits if R and L]
    return switches


def replace_letter(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    splits = [(word[:i],word[i:]) for i in range(len(word))]
    replaces = [L + c + (R[1:] or "") for L,R in splits for c in letters]
    return replaces