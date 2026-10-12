#!/usr/bin/env python3
# Boot the SDK's QEMU image and run a kvmtool guest; usage: kvm_smoke.py <sdk dir>
import os, subprocess, sys, time, select

sdk = sys.argv[1]
inst = f"{sdk}/install64_qemu"
cmd = [f"{sdk}/build64_qemu/host/bin/qemu-system-riscv64", "-M", "virt", "-cpu", "rv64,h=true",
       "-smp", "2", "-m", "2G", "-nographic", "-bios", f"{inst}/fw_dynamic.bin",
       "-kernel", f"{inst}/Image", "-initrd", f"{inst}/rootfs.cpio",
       "-append", "console=ttyS0 earlycon"]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
buf = b""

def expect(pat, timeout):
    global buf
    end = time.time() + timeout
    while time.time() < end:
        if pat.encode() in buf:
            i = buf.index(pat.encode()) + len(pat)
            buf = buf[i:]
            return True
        r, _, _ = select.select([p.stdout], [], [], 1)
        if r:
            d = os.read(p.stdout.fileno(), 4096)
            if not d:
                break
            sys.stdout.write(d.decode(errors="replace")); sys.stdout.flush()
            buf += d
    print(f"\n### TIMEOUT waiting for {pat!r}"); p.kill(); sys.exit(1)

def send(s):
    # one char at a time: the guest's emulated UART drops bursts
    for c in s.encode() + b"\n":
        p.stdin.write(bytes([c])); p.stdin.flush(); time.sleep(0.05)

expect("login:", 600); send("root")
expect("# ", 60)
send("grep -o 'isa.*' /proc/cpuinfo | head -1; ls -l /dev/kvm; dmesg | grep -i kvm")
expect("# ", 60)
send("lkvm run -k /boot/Image -m 256 -c 1 --console serial -p 'console=ttyS0' 2>&1")
expect("Mounting...", 900); expect("/ # ", 120)  # guest shell (kvmtool 9p root)
send("uname -a; cat /proc/cpuinfo | grep -m1 isa; date; sleep 1; date; poweroff -f")
expect("KVM session ended normally", 300)
expect("# ", 60)
send("poweroff")
time.sleep(5); p.kill()
print("\n### BOOT+KVM OK")
