class MissingClosing(RuntimeError):
    pass


class MissingOpening(RuntimeError):
    pass


class NoCentralSymbols(RuntimeError):
    pass


class MultipleCentralSymbols(RuntimeError):
    pass


def auto_swap(s: str) -> str:
    symbols = "=+-*/,"
    openings = "([{<"
    closings = ")]}>"
    assert len(openings) == len(closings)
    strings = "\"'"

    symbol_idx = None
    closure_stack = [0] * len(openings)
    in_string = [False] * len(strings)

    i = 0
    while i < len(s):
        if (j := strings.find(s[i])) != -1:
            in_string[j] = not in_string[j]  # toggle in_string
        else:
            if not any(in_string):
                if (j := openings.find(s[i])) != -1:
                    closure_stack[j] += 1
                elif (j := closings.find(s[i])) != -1:
                    closure_stack[j] -= 1
                    if closure_stack[j] < 0:
                        raise MissingOpening(f"'{closings[j]}' does not match '{openings[j]}' before")
                elif s[i] in symbols and sum(closure_stack) == 0 and sum(in_string) == 0:
                    if symbol_idx is None:
                        symbol_idx = i
                    else:
                        raise MultipleCentralSymbols(f"Multiple central symbols matched ('{s[symbol_idx]}' and '{s[i]}')")
        i += 1

    # Check for remaining closure/string tokens
    for j in range(len(closure_stack)):
        if closure_stack[j] != 0:
            raise MissingClosing(f"'{openings[j]}' does not match '{closings[j]}' afterward")
    for j in range(len(in_string)):
        if in_string[j]:
            raise MissingClosing(f"String '{strings[j]}' does not close")

    if symbol_idx is None:
        raise NoCentralSymbols(f'No central symbol found among "{symbols}"')

    # Extend for spaces before and after
    center_start = symbol_idx
    while center_start > 0 and s[center_start - 1] == ' ':
        center_start -= 1

    center_end = symbol_idx + 1
    while center_end < len(s) and s[center_end] == ' ':
        center_end += 1

    return s[center_end:] + s[center_start:center_end] + s[:center_start]


if __name__ == '__main__':
    import sys
    assert len(sys.argv) == 2
    try:
        print(auto_swap(sys.argv[1]), end="")
    except Exception as e:
        print(f"Error: {e}")
