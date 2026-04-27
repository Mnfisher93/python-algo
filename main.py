# ============================================================================
# 🏁  LESSON 7 LAB — Too Many Algorithms: Race the Sorts!
# ============================================================================
#
# GOAL:
#   Build Quick Sort and Merge Sort functions from scratch, then use
#   cProfile and multiprocessing to race them side-by-side and see
#   which one finishes first.
#
# WHAT YOU WILL LEARN:
#   1. How Merge Sort works (divide → sort halves → merge back together)
#   2. How Quick Sort works (pick a pivot → partition → sort each side)
#   3. How to use cProfile to measure how fast a function runs
#   4. How to use multiprocessing to run two tasks at the SAME TIME
#
# INSTRUCTIONS:
#   - Read every comment carefully.
#   - Type the code yourself — DO NOT just copy-paste! Typing it builds
#     muscle memory and helps you learn.
#   - Run the script when you're done:  python main.py
#
# ============================================================================

# ----------------------------------------------------------------------------
# STEP 1: Import the libraries we need
# ----------------------------------------------------------------------------

import random           # We'll use this to create a random list of numbers
import cProfile         # This lets us "profile" (measure) how fast code runs
import multiprocessing  # This lets us run multiple tasks at the same time
import time             # We'll use this to time the overall program


# ============================================================================
# STEP 2: BUILD THE MERGE SORT FUNCTION
# ============================================================================
#
# HOW MERGE SORT WORKS:
#   1. Take the list and CUT it in half.
#   2. Keep cutting each half until every piece has just 1 item.
#      (A list of 1 item is already sorted!)
#   3. MERGE the pieces back together — always putting the smaller
#      number first.
#
# EXAMPLE:
#   [5, 2, 8, 1]
#       ├── [5, 2]          ← split
#       │   ├── [5]         ← base case (1 item = sorted!)
#       │   ├── [2]         ← base case
#       │   └── merge → [2, 5]
#       ├── [8, 1]          ← split
#       │   ├── [8]         ← base case
#       │   ├── [1]         ← base case
#       │   └── merge → [1, 8]
#       └── merge → [1, 2, 5, 8]   ← DONE!
#
# SPEED: O(n log n) — ALWAYS, even in the worst case. 🎉
# ============================================================================

def merge_sort(arr):
    """
    Sorts a list using the Merge Sort algorithm.

    Parameters:
        arr (list): The list of numbers to sort.

    Returns:
        list: A new sorted list.
    """

    # --- BASE CASE ---
    # If the list has 0 or 1 items, it's already sorted!
    # This is what STOPS the recursion from going forever.
    if len(arr) <= 1:
        return arr

    # --- DIVIDE ---
    # Find the middle index of the list
    mid = len(arr) // 2

    # Split the list into two halves
    left_half = arr[:mid]       # Everything from the start to the middle
    right_half = arr[mid:]      # Everything from the middle to the end

    # --- CONQUER ---
    # Recursively sort each half (this is where the magic happens!)
    # merge_sort calls ITSELF on smaller and smaller pieces
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # --- COMBINE ---
    # Merge the two sorted halves back together
    return merge(sorted_left, sorted_right)


def merge(left, right):
    """
    Merges two SORTED lists into one sorted list.

    Parameters:
        left (list):  A sorted list.
        right (list): Another sorted list.

    Returns:
        list: A single merged, sorted list.
    """

    result = []     # This will hold our merged result
    i = 0           # Pointer for the left list
    j = 0           # Pointer for the right list

    # Walk through both lists at the same time.
    # Compare the current item in each list and pick the smaller one.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            # Left item is smaller (or equal), so add it
            result.append(left[i])
            i += 1      # Move the left pointer forward
        else:
            # Right item is smaller, so add it
            result.append(right[j])
            j += 1      # Move the right pointer forward

    # If there are leftover items in the left list, add them all
    # (They're already sorted, so we can just tack them on)
    result.extend(left[i:])

    # Same for the right list
    result.extend(right[j:])

    return result


# ============================================================================
# STEP 3: BUILD THE QUICK SORT FUNCTION
# ============================================================================
#
# HOW QUICK SORT WORKS:
#   1. Pick one number from the list — this is called the PIVOT.
#   2. Put everything SMALLER than the pivot into a "left" pile.
#   3. Put everything BIGGER than the pivot into a "right" pile.
#   4. Quick Sort each pile recursively.
#   5. Stick them together:  sorted_left + [pivot] + sorted_right
#
# EXAMPLE:
#   quick_sort([5, 2, 8, 1, 6])
#       pivot = 5
#       left  = [2, 1]    (numbers ≤ 5)
#       right = [8, 6]    (numbers > 5)
#       ├── quick_sort([2, 1]) → [1, 2]
#       └── quick_sort([8, 6]) → [6, 8]
#       Final: [1, 2] + [5] + [6, 8] = [1, 2, 5, 6, 8]
#
# SPEED:
#   Average case: O(n log n) — usually the FASTEST sort in practice! ⚡
#   Worst case:   O(n²) — if the pivot is always the smallest or biggest
# ============================================================================

def quick_sort(arr):
    """
    Sorts a list using the Quick Sort algorithm.

    Parameters:
        arr (list): The list of numbers to sort.

    Returns:
        list: A new sorted list.
    """

    # --- BASE CASE ---
    # If the list has 0 or 1 items, it's already sorted!
    if len(arr) <= 1:
        return arr

    # --- PICK A PIVOT ---
    # We'll use the FIRST element as our pivot.
    # (There are fancier ways to pick a pivot, but this is the simplest.)
    pivot = arr[0]

    # --- PARTITION ---
    # Split the remaining items into two groups:
    #   - "less_than" = items that are LESS THAN or EQUAL to the pivot
    #   - "greater_than" = items that are GREATER than the pivot
    rest = arr[1:]      # Everything EXCEPT the pivot

    less_than = []
    greater_than = []

    for item in rest:
        if item <= pivot:
            less_than.append(item)      # Goes to the LEFT pile
        else:
            greater_than.append(item)   # Goes to the RIGHT pile

    # --- RECURSIVE CASE ---
    # Sort each pile, then combine: sorted_left + pivot + sorted_right
    return quick_sort(less_than) + [pivot] + quick_sort(greater_than)


# ============================================================================
# STEP 4: BUILD THE PROFILING FUNCTIONS
# ============================================================================
#
# WHAT IS cProfile?
#   cProfile is a built-in Python tool that measures how many times
#   each function is called and how long it takes. This helps us see
#   which sorting algorithm is faster!
#
# HOW IT WORKS:
#   1. Create a Profile object:      pr = cProfile.Profile()
#   2. Turn it on:                    pr.enable()
#   3. Run the code you want to measure
#   4. Turn it off:                   pr.disable()
#   5. Print the results:             pr.print_stats()
# ============================================================================

def profile_merge_sort(arr):
    """
    Runs Merge Sort on a COPY of the array and profiles it with cProfile.
    We use arr.copy() so the original list stays unchanged.
    """
    print("\n" + "=" * 60)
    print("📊  MERGE SORT — cProfile Results")
    print("=" * 60)

    # Create a cProfile object to measure performance
    pr = cProfile.Profile()

    # Start profiling (like pressing START on a stopwatch)
    pr.enable()

    # Run merge sort on a COPY of the array
    # We use .copy() so the original array isn't changed
    merge_sort(arr.copy())

    # Stop profiling (like pressing STOP on the stopwatch)
    pr.disable()

    # Print the profiling results
    # This shows: how many function calls, how much time, etc.
    pr.print_stats()


def profile_quick_sort(arr):
    """
    Runs Quick Sort on a COPY of the array and profiles it with cProfile.
    We use arr.copy() so the original list stays unchanged.
    """
    print("\n" + "=" * 60)
    print("📊  QUICK SORT — cProfile Results")
    print("=" * 60)

    # Create a cProfile object to measure performance
    pr = cProfile.Profile()

    # Start profiling
    pr.enable()

    # Run quick sort on a COPY of the array
    quick_sort(arr.copy())

    # Stop profiling
    pr.disable()

    # Print the profiling results
    pr.print_stats()


# ============================================================================
# STEP 5: USE MULTIPROCESSING TO RACE THEM!
# ============================================================================
#
# WHAT IS MULTIPROCESSING?
#   Normally, Python runs one thing at a time (like a single chef in a
#   kitchen). Multiprocessing lets you run multiple things at the SAME
#   time (like having two chefs working on different dishes).
#
# WHY USE IT HERE?
#   We want to run Merge Sort and Quick Sort at the same time so we can
#   fairly compare how long each one takes. If we ran them one-after-
#   the-other, the second one might be faster just because the computer
#   had time to "warm up."
#
# HOW IT WORKS:
#   1. Create a Process for each task
#   2. .start() each process (they begin running in parallel)
#   3. .join() each process (wait for them to finish)
# ============================================================================

# This "if __name__ == '__main__':" line is REQUIRED for multiprocessing.
# It tells Python: "Only run this code if I'm running the file directly,
# NOT if I'm importing it from somewhere else."
if __name__ == "__main__":

    # ------------------------------------------------------------------
    # STEP 5a: Generate a random list of 1000 numbers
    # ------------------------------------------------------------------
    # This one-liner creates a list of 1000 random integers between 0-1000
    # It uses a "list comprehension" — a compact way to build a list:
    #   [expression for variable in range(count)]
    arr = [random.randint(0, 1000) for _ in range(1000)]

    # Print a preview so we can see the unsorted data
    print("=" * 60)
    print("🏁  LESSON 7 LAB: Race the Sorting Algorithms!")
    print("=" * 60)
    print(f"\n🎲  Generated {len(arr)} random numbers.")
    print(f"    First 10 numbers: {arr[:10]}")
    print(f"    Last 10 numbers:  {arr[-10:]}")

    # ------------------------------------------------------------------
    # STEP 5b: Create multiprocessing Process objects
    # ------------------------------------------------------------------
    # Each Process will run one of our profiling functions.
    # target = the function to run
    # args   = the arguments to pass to that function (must be a tuple!)
    p1 = multiprocessing.Process(target=profile_merge_sort, args=(arr,))
    p2 = multiprocessing.Process(target=profile_quick_sort, args=(arr,))

    # ------------------------------------------------------------------
    # STEP 5c: Start the timer and launch both processes
    # ------------------------------------------------------------------
    print("\n⏱️   Starting both sorts in parallel using multiprocessing...")
    start_time = time.time()

    # .start() kicks off each process — they run at the SAME TIME!
    p1.start()      # Merge Sort begins running
    p2.start()      # Quick Sort begins running (at the same time!)

    # ------------------------------------------------------------------
    # STEP 5d: Wait for both processes to finish
    # ------------------------------------------------------------------
    # .join() means "wait here until this process is done"
    p1.join()       # Wait for Merge Sort to finish
    p2.join()       # Wait for Quick Sort to finish

    # ------------------------------------------------------------------
    # STEP 5e: Print the total elapsed time
    # ------------------------------------------------------------------
    end_time = time.time()
    total_time = end_time - start_time

    print("\n" + "=" * 60)
    print(f"✅  Both sorts finished!")
    print(f"⏱️   Total elapsed time: {total_time:.4f} seconds")
    print("=" * 60)

    # ------------------------------------------------------------------
    # BONUS: Verify that both sorts produce the same result
    # ------------------------------------------------------------------
    # Let's make sure both algorithms actually sort correctly!
    merge_result = merge_sort(arr.copy())
    quick_result = quick_sort(arr.copy())

    if merge_result == quick_result:
        print("\n✅  Both sorts produced the SAME result — they work!")
    else:
        print("\n❌  The sorts produced DIFFERENT results — something is wrong!")

    # Compare with Python's built-in sort to double-check
    python_sorted = sorted(arr)
    if merge_result == python_sorted and quick_result == python_sorted:
        print("✅  Results match Python's built-in sorted() — perfect!")
    else:
        print("❌  Results don't match Python's built-in sorted() — check your code!")

    print("\n🎓  Great work! You just built two advanced sorting algorithms")
    print("    and raced them using multiprocessing and cProfile!")
    print("=" * 60)


# ============================================================================
# 🧠  CHALLENGE QUESTIONS (discuss with your partner or instructor):
#
#   1. Which sort was faster? Merge Sort or Quick Sort?
#   2. What happens if you change the list size to 10,000? To 100,000?
#   3. Why does cProfile show different numbers of function calls for each?
#   4. What would happen if the list was ALREADY sorted before we ran
#      Quick Sort? Would it still be fast? (Hint: think about the pivot!)
#   5. Python's built-in sorted() uses Timsort — why do you think the
#      language creators chose a merge-style sort?
#
# 🔥  BONUS CHALLENGES:
#   - Add Bubble Sort and Selection Sort to the race. How much slower
#     are they on 1,000 items? On 10,000?
#   - Try changing the pivot in Quick Sort to use the MIDDLE element
#     instead of the first. Does it change the speed?
#   - Use time.time() inside each profiling function to print the exact
#     seconds each sort takes (not just cProfile stats).
# ============================================================================
