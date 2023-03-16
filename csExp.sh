#!/bin/bash
# start overhead
# git pull
echo "$2" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=20 # 20 seconds
threads=500
depth=1500
iterations=10
# define experiment
experiment() {
  # setup
  killall -q python3
  killall -q bpftrace
  truncate -s 0 raw.txt
  sleep 1 # wait for 1 second
  # run tracing if necessary
  if [ "$2" != "X" ]; then
    if [ "$2" == "1" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "2" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "3" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "4" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "5" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "6" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "7" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "8" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "9" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
    if [ "$2" == "10" ]; then
      sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & sudo bpftrace Scripts/A.bt >>raw.txt & # begin tracing
    fi
  fi
  # run the jobs and count how many get done
  end=$((SECONDS + increment))
  counter=0                       # number of fib jobs completed
  truncate -s 0 raw.txt           # clear file
  while [ $SECONDS -lt $end ]; do # continue for 10 seconds
    python3 job.py $counter $threads $depth >>/dev/null &&
      counter=$((counter + 1)) # run job and increment counter
  done
  # end tracing
  killall -q bpftrace
  # update logs
  echo $counter >>Logs/csExp/log_"$1".txt # add jobs done to log
  outputSize=$(wc -l raw.txt)
  echo "$outputSize" >>Logs/csExp/log_"$1".txt                    # add output size to log
  echo "Completed: $counter for $2 with $outputSize events" # output to console
}
# run experiment
echo "Starting experiment ${1}"
iterationCounter=0S
for _ in {1..10}; do # number of iterations
  # warmup phase
  end=$((SECONDS + 5))
  while [ $SECONDS -lt $end ]; do # run 15 seconds of warmup
    python3 job.py "warmup" 20 20 # run job
  done
  # experiment phase
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  experiment "$1" X # base run
  experiment "$1" 1 # 1 context switch
  experiment "$1" 2 # 2 context switch
  experiment "$1" 3 # 3 context switch
  experiment "$1" 4 # 4 context switch
  experiment "$1" 5 # 5 context switch
  experiment "$1" 6 # 6 context switch
  experiment "$1" 7 # 7 context switch
  experiment "$1" 8 # 8 context switch
  experiment "$1" 9 # 9 context switch
  experiment "$1" 10 # 10 context switch
done
python3 process.py "$1" $iterations $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
#python3 visualizer.py "$1" # run number
# git pull
git add .
git commit -m "add and process overhead experiment $1"
# git push # add to git
