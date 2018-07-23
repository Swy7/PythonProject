# 选择排序
def selectSort(listExample):
	listLen = len(listExample)
	for i in range(listLen - 1):
		min_index = i
		for j in range(i + 1, listLen):
			if listExample[min_index] > listExample[j]:
				min_index = j
		if i != min_index:
			listExample[min_index], listExample[i] = listExample[i], listExample[min_index]
	return listExample

#冒泡排序
def bubbleSorted(listExample):
	listLen = len(listExample)
	print(listExample)
	for i in range(listLen - 1):
		for j in range(listLen - 1, i, -1):
			if listExample[j] < listExample[j - 1]:
				listExample[j], listExample[j - 1] = listExample[j - 1], listExample[j]
	return listExample


from collections import deque

#合并排序1
def merge_sort1(lst):
	if len(lst) <= 1:
		return lst

	middle = int(len(lst) // 2)
	left = merge_sort1(lst[:middle])
	right = merge_sort1(lst[middle:])
	return merge1(left, right)


def merge1(left, right):
	merged, left, right = deque(), deque(left), deque(right)
	while left and right:
		merged.append(left.popleft() if left[0] <= right[0] else right.popleft())  # deque popleft is also O(1)
	merged.extend(right if right else left)
	return merged

#合并排序2
def merge_sort2(lst):
	if len(lst) <= 1:
		return lst

	middle = int(len(lst) // 2)
	left = merge_sort2(lst[:middle])
	right = merge_sort2(lst[middle:])
	return merge2(left, right)


def merge2(left, right):
	i, j = 0, 0
	merged = []
	while i < len(left) and j < len(right):
		if left[i] < right[j]:
			merged.append(left[i])
			i += 1
		else:
			merged.append(right[j])
			j += 1
	if i < len(left):
		merged.extend(left[i:])
	if j < len(right):
		merged.extend(right[j:])
	return merged


# 快排
def quick_sort(lst, lo, hi):
	if lo < hi:
		p = partition(lst, lo, hi)
		quick_sort(lst, lo, p)
		quick_sort(lst, p + 1, hi)
	return lst


def partition(lst, lo, hi):
	pivot = lst[lo]
	i = lo
	for j in range(lo+1,hi):
		if lst[j] < pivot:
			i += 1
			if i != j:
				lst[i], lst[j] = lst[j], lst[i]
	if i != lo:
		lst[i], lst[lo] = lst[lo], lst[i]
	return i


if __name__ == '__main__':
	import random
	import time

	lst = random.sample(range(3000000), 1000000)
	# lst = [41,2,34,2,23,21,12,25,12,14,15,12,15,19,56,745,67,433,3478,4534]
	st1 = time.time()
	merge_sort1(lst[:])
	en1 = time.time()
	print('merge_sort1---' + str(en1 - st1))
	st2 = time.time()
	merge_sort2(lst[:])
	en2 = time.time()
	print('merge_sort2--' + str(en2 - st2))
	st3 = time.time()
	quick_sort(lst[:],0,len(lst))
	en3 = time.time()
	print('quick_sort--' + str(en3 - st3))
