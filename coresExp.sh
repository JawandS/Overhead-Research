# machine experiment is being run on
machine="school"

# context switch experiment with variable numeber of cores
cores=0-1
echo "${machine}${cores}_1_per"
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" csExp
sleep 3

cores=0-3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" csExp
sleep 3

cores=0-7
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./csExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" csExp
sleep 3

# probes experiment with variable number of cores
cores=0
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" probesExp
sleep 3

cores=0-1
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" probesExp
sleep 3

cores=0-3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" probesExp
sleep 3

cores=0-7
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_1_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_2_ps" powersave
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_3_per" performance
sleep 3
sudo taskset -c $cores ./probesExp.sh "${machine}${cores}_4_ps" powersave
sleep 3
# visualize results
sudo python3 analyze.py "${machine}${cores}" probesExp
sleep 3