import subprocess
import time
import pyRAPL
import csv

# Setting up pyRAPL
pyRAPL.setup()
csv_output = pyRAPL.outputs.CSVOutput('PyRAPL.csv')

# The command that will be run in the terminal
command = 'taskset -c 0,1,2,3 python3 pypaswas.py --device_type=CPU --platform_name=Intel --framework=opencl test1.fasta test2.fasta'

# Command to run s-tui and monitor CPU power usage
s_tui_command = 's-tui --csv-file CPU_measure.csv'


def kill_process(process):
    if process.poll() is None:  # Check if the process is still running
        try:
            # Try to terminate process
            process.terminate()

            # Wait for up to 5 seconds for the process to terminate
            for _ in range(5):
                if process.poll() is not None:  # If process has ended
                    return
                time.sleep(1)

            # If process is still running after 5 seconds, kill it
            process.kill()
        except Exception as e:
            print(f"Error while terminating process: {e}")



@pyRAPL.measureit(output=csv_output, number=1)
def main():
    start = time.time()
    try:
        # Start s-tui in the background to monitor CPU power usage
        s_tui_process = subprocess.Popen(s_tui_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Run the command in the terminal
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors or exceptions here
        print(f"Command '{command}' failed with error: {e}")

    finally:
        # Stop and kill the s-tui process
        kill_process(s_tui_process)

        # Monitor GPU power consumption using nvidia-smi
        gpu_command = 'nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits'
        try:
            gpu_power_output = subprocess.check_output(gpu_command, shell=True, universal_newlines=True)
            gpu_power = float(gpu_power_output.strip())
            print(f"GPU Power Consumption: {gpu_power} W")

            # Save GPU power consumption to a separate CSV file
            with open('GPU.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([time.time(), gpu_power])
        except subprocess.CalledProcessError as e:
            # Handle errors or exceptions here
            print(f"Command '{gpu_command}' failed with error: {e}")

    end = time.time()
    print(f"Execution Time: {end - start} seconds")


if __name__ == '__main__':
    main()
    csv_output.save()
