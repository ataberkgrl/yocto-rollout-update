meta-rollout is layer for update agent. It depends on meta-openembedded 
layer to use python3-requests recipe. You can find rollout-update agent 
bitbake recipes and 
agent files in this folder with rollout.service script to initialize on boot with systemd. It requests to 192.168.7.1:2333 from qemu to access update server that runs on host machine.

Server directory includes update server components. Server must run on host machine to be able to get requests from update agent on qemu.
