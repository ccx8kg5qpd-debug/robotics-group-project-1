# 机器人集成小组项目1

基于 YOLOv8 和 NVIDIA Jetson Orin NX 的桌面目标检测与 ROS2 发布。

## 项目目标

项目识别两类桌面物体：

- `0 = bottle`
- `1 = mouse`

模型在 Jetson Orin NX 上读取 USB 摄像头画面，实时显示 bounding box、class、confidence 和完整循环 FPS，并通过 ROS2 topic `/qyy/detections` 发布 JSON 检测结果。

## 主要结果

- 最终数据集：1000 张图片、1000 个 YOLO 标注
- 数据组成：30 张自采图片 + 970 张 COCO 2017 图片
- 划分：train 800、val 100、test 100
- 模型：YOLOv8n，100 epochs，imgsz 640
- 推理阈值：`conf=0.70`
- 正式测试：22 个实例，21 个正确，正确率 95.45%
- 完整循环 FPS：16.6-16.9，平均 16.77 FPS
- ROS2 node：`qyy_yolo_detector`
- ROS2 topic：`/qyy/detections`

## 目录

```text
dataset/     数据配置、划分统计、质量检查和来源/许可清单
model/       最终模型 best.pt
program/     Jetson 实时检测与 ROS2 发布程序
results/     训练曲线、测试表和真实正确/错误案例
report/      个人 LaTeX 模板、实验报告 PDF 和报告图片
video/       演示视频参数及内容核验说明
```

完整 1000 图数据集和演示视频随课程提交 ZIP 提交。GitHub 仓库仅保留数据配置、划分清单与逐图来源/许可记录，避免重复发布外部图片以及存放超大视频文件。

## Jetson 运行

```bash
cd ~/qyy_object_detection
source qyy_env/bin/activate
source /opt/ros/humble/setup.bash
python ros2_detect.py
```

另一个终端查看 ROS2 消息：

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /qyy/detections
```

普通实时检测：

```bash
python detect_realtime.py
```

按键：`s` 保存正确案例，`e` 保存错误案例，`q` 退出。

## 数据来源

自采数据为 30 张 iPhone 拍摄图片。其余 970 张来自 COCO 2017，标注由 COCO 官方 instance annotations 转换为 YOLO 格式。外部图片用于课程教学/科研实验，各图片许可信息见 `dataset/source_info/source_manifest.csv`。

## 报告

实验报告使用个人设计的 LaTeX 模板，源文件和编译后的 PDF 位于 `report/`。

项目仓库：<https://github.com/ccx8kg5qpd-debug/robotics-group-project-1>

