# 🏁 Race the Sorts! — Lesson 7 Lab

> **iCode Green Belt · Sprint 3 · Lesson 7: Too Many Algorithms — Merge Sort + Quick Sort**

---

## 🏁 What This Is

A hands-on Python lab where you build **Merge Sort** and **Quick Sort** from scratch, measure their speed with **cProfile**, and race them side-by-side using **multiprocessing** — all in a single file you can run from your terminal. Built for the iCode Green Belt curriculum (Sprint 3, Lesson 7) by tutor **Morgan ([@Mnfisher93](https://github.com/Mnfisher93))**.

---

## 🎯 What You'll Learn

- 🔀 **How Merge Sort works** — divide a list in half, sort each half, then merge them back together.
- ⚡ **How Quick Sort works** — pick a pivot, partition into smaller/bigger piles, and sort each pile recursively.
- 📊 **How to profile code with `cProfile`** — measure how many function calls happen and how long they take.
- 🧵 **How to use `multiprocessing`** — run two tasks at the *same time*, like having two chefs in a kitchen.
- ✅ **How to verify your results** — compare your sorts against Python's built-in `sorted()` to make sure they're correct.

---

## 📦 What's Inside

| File | Description |
|------|-------------|
| `main.py` | The full lab — Merge Sort, Quick Sort, cProfile profiling, and a multiprocessing race on 1,000 random numbers. Read the comments, type the code, and run it! |

---

## 🚀 How to Run

Make sure you have **Python 3** installed, then open a terminal and run:

```bash
python main.py
```

That's it! The script will:

1. Generate **1,000 random numbers** 🎲
2. Launch Merge Sort and Quick Sort **in parallel** using `multiprocessing`
3. Print **cProfile stats** for each sort 📊
4. Show the **total elapsed time** ⏱️
5. Verify both sorts match Python's built-in `sorted()` ✅

---

## 📖 How the Code Is Organized

The file follows a step-by-step structure — each section is clearly labeled with comments:

| Step | What Happens |
|------|-------------|
| **Step 1** | Import `random`, `cProfile`, `multiprocessing`, and `time` |
| **Step 2** | Build the `merge_sort()` and `merge()` functions |
| **Step 3** | Build the `quick_sort()` function |
| **Step 4** | Create `profile_merge_sort()` and `profile_quick_sort()` wrappers that use `cProfile` |
| **Step 5** | Generate random data, start both sorts in parallel with `multiprocessing.Process`, and print results |

---

## 🧠 Challenge Questions

After you run the lab, try discussing these with your partner or instructor:

1. Which sort was faster — Merge Sort or Quick Sort?
2. What happens if you change the list size to **10,000**? To **100,000**?
3. Why does cProfile show different numbers of function calls for each sort?
4. What would happen if the list was *already sorted* before running Quick Sort?
5. Python's built-in `sorted()` uses **Timsort** — why do you think the language creators chose a merge-style sort?

---

## 🔥 Bonus Challenges

- Add **Bubble Sort** and **Selection Sort** to the race. How much slower are they?
- Change Quick Sort's pivot to use the **middle element** instead of the first. Does it change the speed?
- Use `time.time()` inside each profiling function to print the **exact seconds** each sort takes.

---

## 📝 Requirements

- **Python 3.6+** (any recent version works)
- No external packages needed — everything uses the Python standard library (`random`, `cProfile`, `multiprocessing`, `time`)

---

## 🎓 About

This lab is part of the **iCode Green Belt** curriculum.

- **Sprint:** 3 — Algorithms in Programming
- **Lesson:** 7 — Too Many Algorithms: Merge Sort + Quick Sort
- **Author:** Morgan ([@Mnfisher93](https://github.com/Mnfisher93))

Happy sorting! 🏁
