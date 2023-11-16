import numpy as np
import multiprocessing
import time
import subprocess
import csv

with open('CPU2_measure.csv', 'a', newline='') as spreadsheet:
    writer = csv.writer(spreadsheet)
    writer.writerow(['runbreak'])

def get_cpu_cores():
    """Returns the number of CPU cores available."""
    return multiprocessing.cpu_count()

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



def parallel_sw(core_id, x, y):
    """Function for parallel execution of the NW algorithm."""
    return smith_waterman(x, y)


if __name__ == "__main__":
    with open('humangenomelong.txt', 'r') as file:
        humangenomelong = file.read().replace('\n', '').replace(' ', '').upper()
    print(len(humangenomelong))

    with open('humangenomeshort.txt', 'r') as file:
        humangenomeshort = file.read().replace('\n', '').replace(' ', '').upper()
    print(len(humangenomeshort))

    # Inform the user about the number of CPU cores
    num_cores = get_cpu_cores()
    print(f"You have {num_cores} CPU cores.")

    # Ask the user for the number of cores they'd like to use
    while True:
        selected_cores = int(input(f"How many cores would you like to use (max {num_cores})? "))
        if 0 < selected_cores <= num_cores:
            break
        print(
            "Invalid number of cores selected. Please enter a number between 1 and the maximum number of cores available.")

    # Split the humangenomelong into smaller sections
    subsection_length = len(humangenomelong) // selected_cores + len(humangenomeshort)
    splits = [humangenomelong[i:i + subsection_length] for i in range(0, len(humangenomelong), subsection_length)]

    # Adjust selected_cores if there are fewer splits than expected
    selected_cores = min(selected_cores, len(splits))

    # Prepare inputs for multiprocessing
    inputs = [(i, splits[i], humangenomeshort) for i in range(selected_cores)]

    # Start s-tui in the background saving output to csv
    s_tui_process = subprocess.Popen(["s-tui --csv-file CPU2_measure.csv"],shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # Parallel alignment
    with multiprocessing.Pool(selected_cores) as pool:
        start_time = time.time()

        results = pool.starmap(parallel_sw, inputs)

        end_time = time.time()
        elapsed_time = end_time - start_time
    #terminate s-tui
    s_tui_process.terminate()
    print("Results from each core:")
    for res in results:
        print(res)

    totaltime = f"Time taken: {elapsed_time} seconds"
    print(totaltime)
    with open('CPU2_measure.csv', 'a',newline='')as spreadsheet:
        writer = csv.writer(spreadsheet)
        writer.writerow([totaltime])