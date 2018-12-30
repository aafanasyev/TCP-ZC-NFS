#!/bin/bash

clear
echo "This bash script measures read write performance of"
echo "NFSv4.2 server client setup with direct network connection"
echo " "
echo "Reading variables..."

# File size in bytes (2GiB)
#FS=2147483648
FS=524288

# Amount of rounds
ROUNDS=100

# Scale gradation of block size
# "512b","2K" "8K" "32K" "128K" "512K" "2M" "8M" "32M" "128M" "512M"
declare -a BSa=("512" 
		"2048"
		"8192" 
		"32768" 
		"131072"
		)
#		"524288" 
#		"2097152" 
#		"8388608" 
#		"33554432" 
#		"134217728" 
#		"536870912"
#		)

# Kernel version
KERNEL="$(uname -r)"

# File written or read by dd
FILE="/srv/nfs/file"

# results of dd
OUTPUT=$KERNEL-NFS.csv

#echo "syncing time"
#date --set="$(ssh andrey@192.168.2.10 -p 1101 date)"
## declare an array variable

echo "Script sends $FS from NFS client to NFS server"
echo "Each blocksize is repeated $ROUNDS times"
echo "The script starts now."
# $(date +%T.%N)"

for bsi in "${BSa[@]}"
do
   for i in $(seq 1 $ROUNDS)
     do
        echo "Block size $bsi. Round $i. Filesize: $(numfmt --to=iec-i $FS)B. Read/Write"
#        echo "$i Write" >> "$KERNEL"-result.txt
#        dd iflag=dsync if=/dev/zero of=$FILE bs=$bsi count=$(($FS / $bsi)) 2>> $OUTPUT
	wr=$(dd iflag=dsync if=/dev/zero of=$FILE bs=$bsi count=$(($FS / $bsi)) 2>&1)
	wr=$(echo ${wr##*s,})
	wr=$(echo ${wr%B/s})
	wr=$(echo ${wr^^})
	wr=$(numfmt --from=si ${wr//[[:blank:]]/})
        sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"
        sleep 1
#        echo "$i Read" >> "$KERNEL"-result.txt
#        dd oflag=dsync if=$FILE of=/dev/null bs=$bsi 2>> $OUTPUT
	rd=$(dd oflag=sync if=$FILE of=/dev/null bs=$bsi 2>&1)
        rd=$(echo ${rd##*s,})
        rd=$(echo ${rd%B/s})
	rd=$(echo ${rd^^})
	rd=$(numfmt --from=si ${rd//[[:blank:]]/})
        rm -rf $FILE
        sleep 1
	echo "$KERNEL,$FS,$bsi,$i,$rd,$wr">>$OUTPUT
     done
done
echo " "
echo "The script is finished"
