# QEMU board patches

`BR2_GLOBAL_PATCH_DIR` for `BOARD=qemu`: Buildroot applies `<package>/*.patch` in order.

## `qemu/`: xcvhtime model for host QEMU

Exported from the `htime` branch of the QEMU fork (github.com/QDucasse/qemu), based on the
`v10.2.0` tag, the version Buildroot pins. Edit and commit there, never here.

Regenerate after changing the branch, from the SDK root (`QEMU_DIR` is the fork checkout):

```sh
git rm -r -q patches/qemu/qemu
git -C "$QEMU_DIR" format-patch v10.2.0..htime -o "$PWD/patches/qemu/qemu/"
git add patches/qemu/qemu
```

The first step drops the previous export: file names follow commit subjects, so stale patches
would otherwise remain and be applied too.

Buildroot applies patches only on extraction, so rebuild with:

```sh
make -C build64_qemu host-qemu-dirclean host-qemu
```

When Buildroot moves to another QEMU release, rebase the branch onto the new tag and update
`v10.2.0` above.
