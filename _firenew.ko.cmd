cmd_/root/firenew.ko := ld -r -m elf_x86_64 -T /usr/src/linux-headers-3.13.0-24-generic/scripts/module-common.lds --build-id  -o /root/firenew.ko /root/firenew.o /root/firenew.mod.o
