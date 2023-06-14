sudo ip neigh add 192.168.2.20 lladdr 22:22:22:22:22:21 dev enp0s3 nud permanent
sleep 0.01
sudo ip neigh add 192.168.2.21 lladdr 22:22:22:22:22:31 dev enp0s3 nud permanent
ip neigh
sleep 2
sudo ip neigh del 192.168.2.20 dev enp0s3
sleep 0.01
sudo ip neigh del 192.168.2.21 dev enp0s3
