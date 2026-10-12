# xcvhtime patches

Board-independent patches for the CORE-V hidden-time extension. A board uses them by listing this
directory after its own in `BR2_GLOBAL_PATCH_DIR`, e.g.
`BR2_GLOBAL_PATCH_DIR="../patches/qemu ../patches/xcvhtime"`. Wired for `BOARD=qemu` only.

## `linux/`: xcvhtime support in KVM

Exported from the `htime` branch of the Linux fork (github.com/QDucasse/linux-stable), based on
the stable `v7.1.10` tag, the version in `configs/qemu/buildroot64_defconfig`. Edit and commit
there, never here.

Regenerate after changing the branch, from the SDK root (`LINUX_DIR` is the fork checkout):

```sh
git rm -r -q patches/xcvhtime/linux
git -C "$LINUX_DIR" format-patch v7.1.10..htime -o "$PWD/patches/xcvhtime/linux/"
git add patches/xcvhtime/linux
```

As with the first step for QEMU, removing the previous export avoids applying stale patches.
Buildroot applies patches only on extraction, so rebuild with:

```sh
make -C buildroot O="$PWD/build64_qemu" linux-dirclean
make XLEN=64 BOARD=qemu
```

Every hook checks for `xcvhtime` first, so the patched kernel also runs on CPUs without it. The
guest kernel is the same `Image` (`/boot/Image`); KVM does not expose `xcvhtime` to guests.
