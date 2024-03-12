#cat /proc/sys/vm/panic_on_oom
#cat /proc/sys/vm/overcommit_memory
#sudo -s sysctl -w vm.overcommit_memory=2

while true
do
	echo ====================================
	date
	sleep 10
	killall -9 CarlaUE4-Linux-Shipping
	sleep 10
	# Launch CARLA (change path accordingly)
	./../../../../carla/CarlaUE4.sh -RenderOffScreen &
	sleep 10
	# Run python code to generate a sequence of dataset (change argument, especially output path accordingly)
	python3 generate_dataset.py --nb_seq 1 --nb_frames 7200 --fps 1 --map Town12 --dynamic_weather False --output_folder /my/output/path
	sleep 10
done

