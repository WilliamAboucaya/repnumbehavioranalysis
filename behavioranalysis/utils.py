import math


GOVERNMENT_ID = 12


def sort_dict_by_value(dict):
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}


def compute_similarity_ratio(list1, list2, ratio):
    m1 = len(list1)
    m2 = len(list2)

    m_inter = len(set(list1[-1:math.floor(-m1 * ratio):-1]) & set(list2[-1:math.floor(-m2 * ratio):-1]))
    m_union = len(set(list1[-1:math.floor(-m1 * ratio):-1]) | set(list2[-1:math.floor(-m2 * ratio):-1]))

    return m_inter / m_union
