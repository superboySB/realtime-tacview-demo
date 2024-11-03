# Tacview实时遥测功能
实现了基于tacview实时遥测功能，具体地，需要先打开tacview的实时遥测功能（端口最好是5555，ip为本地，用户名随意），看到等待标志以后，我们运行下面的python脚本
```sh
python udp_demo_for_tacview
```
在确保tacview的5555端口打开的情况下,可以看到飞机和tacview基本是实时联动的。