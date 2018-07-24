# def two_sum(nums,target):
#     for i in range(len(nums)):
#         search_nubm = target - nums[i]
#         if search_nubm in nums[i + 1:]:
#             new_array = nums[i + 1:]
#             print ([i, i + 1+ new_array.index(search_nubm)])

def two_sum(nums, target):
    numbs_dict = dict()
    for i in range(len(nums)):
        if (target - nums[i]) in numbs_dict:
            return numbs_dict[target - nums[i]], i
        else:
            numbs_dict[nums[i]] = i


def reverse(x):
    numb_str = str(x)
    if x < 0:
        reversed_numb = int('-' + numb_str[:-len(numb_str):-1])
    else:
        reversed_numb = int(numb_str[::-1])
    if pow(-2, 31) <= reversed_numb <= pow(2, 31) - 1:
        return reversed_numb
    else:
        return 0


def isPalindrome(x):
    if x < 0:
        return False
    else:
        return str(x) == str(x)[::-1]


def romanToInt(s):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    sums = 0
    for i in range(len(s)):
        numb = roman_dict[s[i]]
        if (i + 1) < len(s):
            if roman_dict[s[i]] < roman_dict[s[i + 1]]:
                numb = -numb
        sums += numb
    return sums


def longestCommonPrefix(strs):
    if len(strs) == 0:
        return ''
    elif len(strs) == 1 or strs[0] == '':
        return strs[0]
    else:
        common_perfix = ''
        n = 0
        index = 0
        while 0 <= n < len(strs[0]):
            perdix = strs[0][index]
            common_perfix += perdix
            for i in strs[1:]:
                if not (i.startswith(common_perfix)):
                    n = -10
                    common_perfix = common_perfix[:-1]
                    break
            index += 1
            n += 1
        return common_perfix


def isValid(s):
    pars = [None]
    parmap = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in parmap and parmap[c] == pars[-1]:
            pars.pop()
        else:
            pars.append(c)
    return len(pars) == 1


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def mergeTwoLists(l1, l2):
    if not l1 and not l2:
        return
    result = ListNode(0)
    l = result
    while l1 and l2:
        if l1.val < l2.val:
            l.next = l1
            l1 = l1.next
        else:
            l.next = l2
            l2 = l2.next
        l = l.next
    l.next = l1 or l2
    return result.next


def removeDuplicates(nums):
    j = 0
    for i in range(len(nums)):
        if nums[j] != nums[i]:
            nums[j + 1], nums[i] = nums[i], nums[j + 1]
            j += 1
    return j + 1


def removeElement(nums, val):
    j = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[j], nums[i] = nums[i], nums[j]
            j += 1
    return j


def strStr(haystack, needle):
    return haystack.find(needle)


def searchInsert(nums, target):
    if target in nums:
        return nums.index(target)
    elif len(nums) == 0:
        return 0
    elif target < nums[0]:
        return 0
    elif target > nums[-1]:
        return len(nums)
    else:
        index = None
        for i in range(len(nums) - 1):
            if nums[i] < target < nums[i + 1]:
                index = i + 1
                break
        return index


def countAndSay(n):
    if n == 1:
        return '1'
    if n > 1:
        i = 1
        next_say = '1'
        while i < n:
            next_say = getSay(next_say)
            i += 1
        return next_say


def getSay(pre_say):
    if str == '1':
        return '11'
    else:
        next_say = ''
        count = 0
        for i in range(len(pre_say)):
            if i + 1 == len(pre_say):
                sign = False
            elif pre_say[i] != pre_say[i + 1]:
                sign = False
            else:
                sign = True
            if sign:
                count += 1
            else:
                next_say += (str(count + 1) + pre_say[i])
                count = 0
        return next_say
