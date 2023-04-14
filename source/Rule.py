def Rule(ranges, max_size):
    t = {}
    for range in ranges:
        t[range.txt] = t[range.txt] if range.txt in t else []
        t[range.txt].append({"lo": range.lo, "hi": range.hi, "at": range.at})
    return prune(t, max_size)

def prune(rule, max_size):
    n = 0
    n_rule = {}
    for txt, ranges in rule.items():
        n += 1
        if len(ranges) == max_size[txt]:
            n=n-1
            rule[txt] = None
        else:
            n_rule[txt] = ranges
    if n > 0:
        return n_rule
    return None