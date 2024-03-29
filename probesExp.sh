#!/bin/bash
# start overhead
git pull
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
    # shellcheck disable=SC2024
    sudo bpftrace ProbeScripts/"$2".bt >>raw.txt & # being tracing
  fi
  # run the jobs and count how many get done
  end=$((SECONDS + increment))
  counter=0                       # number of fib jobs completed
  truncate -s 0 raw.txt           # clear file
  while [ $SECONDS -lt $end ]; do # continue for 20 seconds
    startTs=$SECONDS
    python3 job.py $counter $threads $depth >>/dev/null && counter=$((counter + 1)) # run job and increment counter
    endTs=$((SECONDS-startTs))
    echo "$endTs" >>Logs/probesExp/tsLog_"$1".txt # add time to log
  done
  # end tracing
  killall -q bpftrace
  # update logs
  echo $counter >>Logs/probesExp/log_"$1".txt # add jobs done to log
  outputSize=$(wc -l raw.txt)
  echo "$outputSize" >>Logs/probesExp/log_"$1".txt                    # add output size to log
  echo "Completed: $counter for $2 with $outputSize events" # output to console
}
# run experiment
iterationCounter=0
for _ in {1..10}; do # number of iterations
  # warmup phase
  end=$((SECONDS + 5))
  while [ $SECONDS -lt $end ]; do # run 15 seconds of warmup
    python3 job.py "warmup" 20 20 # run job
  done
  # experiment phase
  iterationCounter=$((iterationCounter + 1)) && printf "\t---------Run %s---------\n" "$iterationCounter"
  experiment "$1" X # X
  experiment "$1" A # rcu:rcu_utilization
  experiment "$1" B # syscalls:sys_enter_nanosleep
  experiment "$1" C # sched:sched_switch
  experiment "$1" D # sched:sched_wakeup
  experiment "$1" E # timer:time_start
  experiment "$1" F # cpu:cpuhp_enter
  experiment "$1" G # syscalls:sys_enter_getcpu
done
python3 processProbes.py "$1" $iterations $increment $threads $depth "$2" # run number, iterations, time, threads, depth, governor
#python3 visualizer.py "$1" # run number
git pull
git add .
git commit -m "add and process overhead experiment $1"
git push # add to git
