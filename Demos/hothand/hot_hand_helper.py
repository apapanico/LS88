import numpy as np
import random


def shuffle(s):
    ell = list(s)
    random.shuffle(ell)
    return ''.join(ell)


def longest_streak(seq, match='1'):
    key = '0' if match == '1' else '1'
    return max(map(len, seq.split(key)))


def longest_two_streaks(seq, match='1'):
    key = '0' if match == '1' else '1'
    return sum(sorted(map(len, seq.split(key)))[-2:])


def num_matches(s, sub):
    n = len(sub)
    ct = 0
    for i in range(len(s) - n + 1):
        if s[i:i + n] == sub:
            ct += 1
    return ct


def count_conditional(shots, conditioning_set):
    base = f'{conditioning_set}'
    conditional_hits = num_matches(shots, base + '1')
    conditional_misses = num_matches(shots, base + '0')
    return conditional_hits, conditional_misses


def compute_t_k_hit(shots, k=2):
    if len(shots) <= k:
        return 0, 0
    hits, misses = count_conditional(shots, '1' * k)
    k_hits = hits + misses
    return hits / k_hits if k_hits > 0 else None


def compute_t_k_miss(shots, k=2):
    if len(shots) <= k:
        return 0, 0
    hits, misses = count_conditional(shots, '0' * k)
    k_misses = hits + misses
    return hits / k_misses if k_misses > 0 else None


def compute_t_k(shots, k=2):
    hits_after_k_hits, H_k = compute_t_k_hit(shots, k=k)
    hits_after_k_misses, M_k = compute_t_k_miss(shots, k=k)
    if H_k > 0 and M_k > 0:
        t_k_hit = hits_after_k_hits / H_k if H_k > 0 else 0
        t_k_miss = hits_after_k_misses / M_k if M_k > 0 else 0
        t_k = t_k_hit - t_k_miss
    else:
        t_k_hit = t_k_miss = t_k = None
    return t_k_hit, t_k_miss, t_k


def compute_t_2(shots):
    return compute_t_k(shots, k=2)


def compute_t_3(shots):
    return compute_t_k(shots, k=3)


def coin_flips(n_flips, prob_heads):
    return np.random.binomial(n_flips, prob_heads)
