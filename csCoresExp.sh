# cores = range i.e. 0-1
$cores=0,1
sudo taskset -c $cores ./csExp.sh 'school"$cores"_1_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_2_ps' powersave
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_3_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_4_ps' powersave
sleep(3)
$cores=0,1,2,3
sudo taskset -c $cores ./csExp.sh 'school"$cores"_1_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_2_ps' powersave
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_3_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_4_ps' powersave
sleep(3)
$cores=0,1,2,3,4,5,6,7
sudo taskset -c $cores ./csExp.sh 'school"$cores"_1_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_2_ps' powersave
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_3_per' performance
sleep(3)
sudo taskset -c $cores ./csExp.sh 'school"$cores"_4_ps' powersave
sleep(3)