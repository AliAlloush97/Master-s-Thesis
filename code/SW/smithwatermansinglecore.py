import numpy as np
import subprocess
import time
import csv

def smith_waterman(x, y, match=1, mismatch=-1, gap=-1):
    nx = len(x)
    ny = len(y)

    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))

    # Pointers to trace through an optimal alignment.
    P = np.zeros((nx + 1, ny + 1))

    # Variables to remember the maximum score position for backtracking
    max_score = 0
    max_pos = (0, 0)

    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if x[i] == y[j]:
                t[0] = F[i, j] + match
            else:
                t[0] = F[i, j] + mismatch
            t[1] = F[i, j + 1] + gap
            t[2] = F[i + 1, j] + gap

            # Added step to reset negative scores to zero for local alignment
            tmax = max(0, np.max(t))
            F[i + 1, j + 1] = tmax
            if tmax > max_score:
                max_score = tmax
                max_pos = (i + 1, j + 1)

            if t[0] == tmax:
                P[i + 1, j + 1] += 2
            if t[1] == tmax:
                P[i + 1, j + 1] += 3
            if t[2] == tmax:
                P[i + 1, j + 1] += 4

    # Trace through an optimal alignment.
    i, j = max_pos
    rx = []
    ry = []
    while i > 0 or j > 0:
        if F[i, j] == 0:  # Stop backtracking at a cell with a score of 0
            break
        if P[i, j] in [2, 5, 6, 9]:
            rx.append(x[i - 1])
            ry.append(y[j - 1])
            i -= 1
            j -= 1
        elif P[i, j] in [3, 5, 7, 9]:
            rx.append(x[i - 1])
            ry.append('-')
            i -= 1
        elif P[i, j] in [4, 6, 7, 9]:
            rx.append('-')
            ry.append(y[j - 1])
            j -= 1

    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    return '\n'.join([rx, ry])


if __name__ == "__main__":
    with open('CPU1_measure.csv', 'a',newline='')as spreadsheet:
        writer = csv.writer(spreadsheet)
        writer.writerow(['runbreak'])

    with open('humangenomelong.txt', 'r') as file:
        humangenomelong = file.read().replace('\n', '').replace(' ', '').upper()
    print(len(humangenomelong))

    with open('humangenomeshort.txt', 'r') as file:
        humangenomeshort = file.read().replace('\n', '').replace(' ', '').upper()
    print(len(humangenomeshort))

    start_time = time.time()
    s_tui_process = subprocess.Popen(["s-tui --csv-file CPU1_measure.csv"],shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    smith_waterman(humangenomelong,humangenomeshort)
    end_time = time.time()
    s_tui_process.terminate()
    elapsed_time = end_time - start_time
    totaltime = f"Time taken: {elapsed_time} seconds"
    print(totaltime)
    with open('CPU1_measure.csv', 'a',newline='')as spreadsheet:
        writer = csv.writer(spreadsheet)
        writer.writerow([totaltime])
