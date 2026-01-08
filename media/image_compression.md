### list_transpoerts
```bash
Declared transports:
image_transport/compressed
image_transport/compressedDepth
image_transport/ffmpeg
image_transport/raw
image_transport/theora

Details:
----------
"image_transport/compressed"
 - Provided by package: compressed_image_transport
 - Publisher: 
      This plugin publishes a CompressedImage using either JPEG or PNG compression.
    
 - Subscriber: 
      This plugin decompresses a CompressedImage topic.
    
----------
"image_transport/compressedDepth"
 - Provided by package: compressed_depth_image_transport
 - Publisher: 
      This plugin publishes a compressed depth images using PNG compression.
    
 - Subscriber: 
      This plugin decodes a compressed depth images.
    
----------
"image_transport/ffmpeg"
 - Provided by package: ffmpeg_image_transport
 - Publisher: 
      This plugin encodes frames into ffmpeg compressed packets
    
 - Subscriber: 
      This plugin decodes frames from ffmpeg compressed packets
    
----------
"image_transport/raw"
 - Provided by package: image_transport
 - Publisher: 
      This is the default publisher. It publishes the Image as-is on the base topic.
    
 - Subscriber: 
      This is the default pass-through subscriber for topics of type sensor_msgs/Image.
    
----------
"image_transport/theora"
 - Provided by package: theora_image_transport
 - Publisher: 
      This plugin publishes a video packet stream encoded using Theora.
    
 - Subscriber: 
      This plugin decodes a video packet stream encoded using Theora.
```
## 🎮 How to use
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
ros2 run image_transport republish raw compressedDepth --ros-args --remap in:=/camera/depth/image_raw --remap out/compressedDepth:=/camera/depth/compressed
```