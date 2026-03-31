# SLAM -> Simultaneous Localization and Mapping

## NEEDS GUI features to see video or image
- `sudo apt update` -> this is needed when in container
- `sudo apt install -y libgl1 libglib2.0-0`
- if `"Could not load the Qt platform plugin "xcb""` error 
  - use: `sudo apt-get install -y libxcb-xinerama0 libqt5gui5 libqt5widgets5 libqt5core5a libgl1-mesa-glx`
- if `"[Open3D WARNING] GLFW Error: Wayland: The platform does not support setting the window position [Open3D WARNING] Failed to initialize GLEW."` error
  - use: `export XDG_SESSION_TYPE=x11`

## TODO
- feature extraction -> identify points in the image that are trackable -- **WORKS!**
- feature matching -> try to find same points from previous frame to next frame -- **WORKS!**
- camera_movement -> ...

### NOTES
- cv2 (opencv) is computer vision library, contains over 2500 algorithms https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
- using flask is silly...
- check out NORM_HAMMING method!!

### stuff 
**enable ssh on windows powershell**
```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
Get-Service ssh-agent
```

**add key to windows**
**powershell**
```powershell
ssh-add $env:USERPROFILE\.ssh\file_name
```

**restart vscode**