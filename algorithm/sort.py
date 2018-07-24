# 选择排序
def selection_sort(lst):
    lst_len = len(lst)
    for i in range(lst_len - 1):
        min_index = i
        for j in range(i + 1, lst_len):
            if lst[min_index] > lst[j]:
                min_index = j
        if i != min_index:
            lst[min_index], lst[i] = lst[i], lst[min_index]
    return lst


# 冒泡排序
def bubble_sorted(lst):
    lst_len = len(lst)
    for i in range(lst_len - 1):
        for j in range(lst_len - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


# 插入排序
def insertion_sort(lst):
    lst_len = len(lst)
    for i in range(1, lst_len):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            else:
                break
    return lst


from collections import deque


# 合并排序
def merge_sort(lst):
    if len(lst) <= 1:
        return lst

    middle = int(len(lst) // 2)
    left = merge_sort(lst[:middle])
    right = merge_sort(lst[middle:])
    return merge(left, right)


def merge(left, right):
    merged, left, right = deque(), deque(left), deque(right)
    while left and right:
        merged.append(left.popleft() if left[0] <= right[0] else right.popleft())  # deque popleft is also O(1)
    merged.extend(right if right else left)
    return merged


# def merge(left, right):
# 	i, j = 0, 0
# 	merged = []
# 	while i < len(left) and j < len(right):
# 		if left[i] < right[j]:
# 			merged.append(left[i])
# 			i += 1
# 		else:
# 			merged.append(right[j])
# 			j += 1
# 	if i < len(left):
# 		merged.extend(left[i:])
# 	if j < len(right):
# 		merged.extend(right[j:])
# 	return merged


# 快排
def quick_sort(lst, lo, hi):
    if lo < hi:
        p = partition(lst, lo, hi)
        quick_sort(lst, lo, p)
        quick_sort(lst, p + 1, hi)
    return lst


# quick_sort(lst, 0, len(lst))
def partition(lst, lo, hi):
    pivot = lst[lo]
    i = lo
    for j in range(lo + 1, hi):
        if lst[j] < pivot:
            i += 1
            if i != j:
                lst[i], lst[j] = lst[j], lst[i]
    if i != lo:
        lst[i], lst[lo] = lst[lo], lst[i]
    return i


# quick_sort(lst, 0, len(lst)-1)
# def partition(lst, lo, hi):
#     pivot = lst[lo]
#     while lo < hi:
#         while lo < hi and lst[hi] >= pivot:
#             hi -= 1
#         lst[lo] = lst[hi]
#         while lo < hi and lst[lo] <= pivot:
#             lo += 1
#         lst[hi] = lst[lo]
#     lst[lo] = pivot
#     return lo


if __name__ == '__main__':
    # import random
    # import time

    # lst = random.sample(range(3000000), 1000000)
    lst = [41,2,34,2,23,21,11,25,10,14,15,12,15,19,56,74,67,33,48,454]
    # st1 = time.time()
    # merge_sort(lst[:])
    # en1 = time.time()
    # print('merge_sort---' + str(en1 - st1))
    # st3 = time.time()
    # quick_sort(lst[:], 0, len(lst))
    # en3 = time.time()
    # print('quick_sort--' + str(en3 - st3))
    print(selection_sort(lst[:]))
    print(bubble_sorted(lst[:]))
    print(insertion_sort(lst[:]))
    print(merge_sort(lst[:]))
    print(quick_sort(lst[:],0,len(lst)))
