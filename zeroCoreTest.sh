#!/bin/bash
# run experiment: sudo ./zeroCoreTest.sh schoolZCT_1_ps powersave
# git pull
echo "$2" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor # powersave or performance
increment=20 # 20 seconds
threads=500
depth=1500
iterations=10
# define experiment
experiment() {
  # change threads
  threads=$3
  # setup
  killall -q python3
  killall -q bpftrace
  truncate -s 0 raw.txt
  sleep 1 # wait for 1 second
  # run the jobs and count how many get done
  end=$((SECONDS + increment))
  counter=0                       # number of fib jobs completed
  truncate -s 0 raw.txt           # clear file
  while [ $SECONDS -lt $end ]; do # continue for 20 seconds
    startTs=$SECONDS
    python3 job.py $counter $threads $depth >>/dev/null && counter=$((counter + 1)) # run job and increment counter
    endTs=$((SECONDS-startTs))
    echo "$endTs" >>Logs/csExp/tsLog_"$1".txt # add time to log
  done
  # end tracing
  killall -q bpftrace
  # update logs
  echo $counter >>Logs/csExp/log_"$1".txt # add jobs done to log
  echo 0 >>Logs/csExp/log_"$1".txt                    # add output size to log
  echo "Completed: $counter for $3 threads" # output to console
}
# run experiment
echo "Starting experiment ${1}"
iterationCounter=0
for _ in {1..5}; do # number of iterations
  # warmup phase
  end=$((SECONDS + 5))
  while [ $SECONDS -lt $end ]; do # run 15 seconds of warmup
    python3 job.py "warmup" 20 20 # run job
  done
  # experiment phase
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  sudo taskset -c 0 experiment "$1" X 200
  sudo taskset -c 0 experiment "$1" X 100
  sudo taskset -c 0 experiment "$1" X 10
  sudo taskset -c 0 experiment "$1" X 1
done
python3 process.py "$1" $iterations $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
# git pull
git add .
git commit -m "add and process zero core test experiment $1"
# git push # add to git
