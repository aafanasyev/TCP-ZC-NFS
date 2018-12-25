# TCP-ZC-NSF
Linux TCP zero-copy: NFS v4.2 performance evaluation.

This project focus on evaluating peformance of NFS after applying a TCP Zero-Copy receive [[1](https://kernelnewbies.org/Linux_4.18#Zero-copy_TCP_receive_API)] in kernel 4.18 and zero copy from user memory to sockets in 4.14 [[2](https://kernelnewbies.org/Linux_4.14#Zero-copy_from_user_memory_to_sockets)]. This makes zero-copy networking possible.

This research is done on Ubuntu server 18.04 LTS. The previous LTS version is 16.04. This is the first version which uses for linux kernel version 4.x [[3](https://wiki.ubuntu.com/Kernel/Support)]. All releases of 16.04.x are available for download[[5](http://old-releases.ubuntu.com/releases/xenial/)].

Network File System (NFS) Version 4 Minor Version 2 Protocol is defined in RFC7862[[6]()]. This is most recent standard released on november 2016. The standard strongly recomended to use a TCP as a transport since NFS version 4 minor 1 [[7](https://tools.ietf.org/html/rfc5661)]. Since Linux kernel 4.0 the NFS server defaults to NFS v4.2 [[8](https://kernelnewbies.org/Linux_4.0#Support_Parallel_NFS_server.2C_default_to_NFS_v4.2)].

[Wiki](https://github.com/aafanasyev/TCP-ZC-NSF/wiki) of this repository contains all practical steps related this research.
