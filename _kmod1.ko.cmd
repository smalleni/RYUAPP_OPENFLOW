cmd_/root/kmod1.ko := ld -r -m elf_x86_64 -T /usr/src/linux-headers-3.13.0-24-generic/scripts/module-common.lds --build-id  -o /root/kmod1.ko /root/kmod1.o /root/kmod1.mod.o
