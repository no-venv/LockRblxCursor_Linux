# LockRblxCursor_Linux

Python script to lock your cursor on waydroid sessions

This only works on X window clients, I don't know how to get the window geometry universally on wayland desktops

As a result, install `weston` for your distro and run waydroid through there. Then run the script on the weston window.

# Dependencies

- pynput
- xdotool

# Install

If you have git installed, you can run:
`git clone https://github.com/no-venv/LockRblxCursor_Linux` 

to clone this git repository or download this as a zip.

# Configuration 

You can configure the script by editing the file, `settings.cfg`

```
keybind=<ctrl>+<shift>+o
edge-offset=20
```

### keybind

You can change your keybind to pause the cursor locking.

For special keys (ctrl, shift and tab, for example) inclose them in <> brackets:

`<ctrl> or <shift> or <tab>`

and to add multiple keys together, add the plus sign in between:

``<ctrl>+a+b``

### edge-offset

You can change `edge-offset` to keep further keep the cursor enclosed.

( if for some reason the cursor doesn't wrap around the edges )

Higher `edge-offset` will keep the cursor more enclosed, but camera movements may become less smoother 

