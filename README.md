# Overhead-Research

### Calculating the overhead cost of using eBPF tracing on throughput

# File/Folder Descriptions

- ### `README.md` - This file
- ### `exp.sh` - Script to run the experiment
    - ### Arguments: run_id governor [powersave, performance, X]
    - ### Example: `sudo ./exp.sh 1 powersave`
    - ### Note: governor may not be accessible on all systems
    - ### Output: Logs/logs_run_id.txt
- ### `process.py` - Script to process the output of the experiment
    - ### Arguments: run_id iterations time_per_run workload_threads workload_depth governor
    - ### Example: `python3 process.py A 10 20 500 1000 powersave`
    - ### Output: Results/results_run_id.txt
    - ### Note: This script is run automatically as part of `exp.sh`
- ### `visualizer.py` - Script to visualize the results of the experiment
    - ### Arguments: run_id
    - ### Example: `python3 visualize.py A`
    - ### Outputs: Figures/run_id_probes.png and Figures/run_id_events.png
    - ### Note: This script is run automatically as part of `exp.sh
- ### `Scripts/` - bpftrace scripts used to test the effect of increasing the number of context switch probes
- ### `ProbeScripts/` - bpftrace scripts used to test different types of probes

# Experiment Setup Commands

`sudo apt update; sudo apt upgrade -y; sudo apt autoremove -y; sudo apt install bpftrace pip -y && sudo pip install matplotlib seaborn pandas scikit-learn; git clone https://github.com/JawandS/Overhead-Research`  
`cd Overhead-Research; sudo chmod u+x exp.sh; sudo git config --global --add safe.directory [directory]`