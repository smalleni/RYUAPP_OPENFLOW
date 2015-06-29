#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x2b22e0c3, __VMLINUX_SYMBOL_STR(module_layout) },
	{ 0xdbd01f1a, __VMLINUX_SYMBOL_STR(netlink_kernel_release) },
	{ 0x47233664, __VMLINUX_SYMBOL_STR(__netlink_kernel_create) },
	{ 0xd7a1ceb0, __VMLINUX_SYMBOL_STR(init_net) },
	{ 0x5644fe73, __VMLINUX_SYMBOL_STR(netlink_unicast) },
	{ 0x66b6ccbe, __VMLINUX_SYMBOL_STR(__nlmsg_put) },
	{ 0x8cb77719, __VMLINUX_SYMBOL_STR(__alloc_skb) },
	{ 0xf366d63f, __VMLINUX_SYMBOL_STR(flag) },
	{ 0x27e1a049, __VMLINUX_SYMBOL_STR(printk) },
	{ 0xf9a482f9, __VMLINUX_SYMBOL_STR(msleep) },
	{ 0xbdfb6dbb, __VMLINUX_SYMBOL_STR(__fentry__) },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=firenew";


MODULE_INFO(srcversion, "BEE9BE1C66C756B35570B2B");
