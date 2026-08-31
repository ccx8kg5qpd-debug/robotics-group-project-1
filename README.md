# Robotics Integration Group Project 1

**Author:** Yongyue Qi

**Repository:** <https://github.com/ccx8kg5qpd-debug/robotics-group-project-1>

This project implements real-time desktop object detection with YOLOv8 on an NVIDIA Jetson Orin NX and publishes structured detection results through ROS2.

## Detection classes

- `0 = bottle`
- `1 = mouse`

The Jetson application displays bounding boxes, class names, confidence values, and full-loop FPS. The ROS2 program publishes the same detections as JSON on `/qyy/detections`.

## Verified results

- Dataset: 1,000 images and 1,000 YOLO label files
- Data composition: 30 self-captured images and 970 COCO 2017 images
- Split: 800 train, 100 validation, and 100 test images
- Model: YOLOv8n, 100 epochs, image size 640
- Final inference threshold: `conf=0.70`
- Validation of `best.pt`: mAP50 0.555 and mAP50-95 0.405
- Final Jetson test: 17 correct frames out of 20, accuracy 85.00%
- Full-loop speed: 16.7-25.8 FPS, mean 22.20 FPS
- ROS2 node: `qyy_yolo_detector`
- ROS2 topic: `/qyy/detections`

## Repository structure

```text
dataset/     Dataset configuration, split reports, validation, and source records
model/       Final YOLOv8 model: best.pt
program/     Real-time Jetson detection and ROS2 publishing programs
results/     Training curves, formal test table, and saved Jetson cases
report/      Final English experimental report and supporting figures
video/       Verified metadata for the submitted demonstration video
```

The complete 1,000-image dataset and demonstration video are included in the course submission package. The repository contains the dataset configuration, split manifest, quality report, and per-image source and licence records.

## Jetson environment

The verified deployment used:

- NVIDIA Jetson Orin NX
- Ubuntu 22.04.5 LTS
- JetPack 6.2.1 / L4T R36.4.4
- Python 3.10.12
- ROS2 Humble
- CUDA 12.6 compatible ARM64 PyTorch
- Ultralytics and OpenCV

## Run real-time detection

```bash
cd ~/qyy_object_detection
source qyy_env/bin/activate
python detect_realtime.py
```

Controls:

- `s`: save a correct case
- `e`: save an error or missed-detection case
- `q`: quit

## Run ROS2 detection

```bash
cd ~/qyy_object_detection
source qyy_env/bin/activate
source /opt/ros/humble/setup.bash
python ros2_detect.py
```

In a second terminal:

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /qyy/detections
```

Published JSON format:

```json
{
  "fps": 18.2,
  "detections": [
    {
      "class": "bottle",
      "confidence": 0.93,
      "bbox": [100, 100, 300, 400]
    }
  ]
}
```

The numbers above illustrate the message schema and are not formal test measurements.

## Dataset provenance

The 30 self-captured images were photographed with an iPhone. The remaining 970 images come from COCO 2017, and their official instance annotations were converted to YOLO format. Individual image source URLs and licence information are recorded in `dataset/source_info/source_manifest.csv`.

External public data were used for course teaching and research. Licence conditions differ between individual images; consult the accompanying source manifest before redistribution.

## Report

The final English PDF report is located in `report/Final_Report.pdf`. It uses an original LaTeX layout prepared for this project and includes the repository link and commit-history evidence.
