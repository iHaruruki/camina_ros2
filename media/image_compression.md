### libx264
```bash
ros2 run image_transport republish raw --ros-args --remap in:=/camera/color/image_raw --remap out:=/camera/color/compressed
```

### H.265(HEVC)
```bash
ros2 run image_transport republish raw ffmpeg --ros-args --remap in:=/image_raw --remap out:=/camera/color/ffmpeg -r __node:=ffmpeg_repub -p out.ffmpeg.encoder:=libx265
```

### Depth
```bash
ros2 run image_transport republish raw compressedDepth   --ros-args   --remap in:=/camera_rear/depth/image_raw   --remap out/compressedDepth:=/camera_rear/depth/compressed
```