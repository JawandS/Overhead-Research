# cores = range i.e. 0-1
sudo taskset -c $cores ./csExp.sh 'school"$cores"_1_per' performance
sleep(15)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_2_ps' powersave
sleep(15)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_3_per' performance
sleep(15)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_4_ps' powersave