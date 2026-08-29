import cv2
import time
import os
from datetime import datetime
from collections import deque
from ultralytics import YOLO

# 加载模型
model = YOLO("best.pt")

# 创建结果目录
correct_dir = "results/correct_cases"
error_dir = "results/error_cases"

os.makedirs(correct_dir, exist_ok=True)
os.makedirs(error_dir, exist_ok=True)

# 打开摄像头
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 用最近30帧计算平均FPS
frame_times = deque(maxlen=30)

print("程序已启动")
print("按 s：保存正确案例")
print("按 e：保存错误案例")
print("按 q：退出")

while True:
    start_time = time.time()

    ret, frame = cap.read()

    if not ret:
        print("无法读取摄像头画面")
        break

    # YOLO检测
    results = model.predict(
        frame,
        conf=0.70,
        device=0,
        verbose=False
    )

    # 绘制检测框、类别和置信度
    annotated_frame = results[0].plot()

    # 计算完整实时FPS
    frame_time = time.time() - start_time
    frame_times.append(frame_time)

    avg_time = sum(frame_times) / len(frame_times)
    fps = 1.0 / avg_time

    # FPS显示
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # 操作提示
    cv2.putText(
        annotated_frame,
        "S: Save Correct | E: Save Error | Q: Quit",
        (20, annotated_frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    cv2.imshow("QYY Object Detection", annotated_frame)

    key = cv2.waitKey(1) & 0xFF

    # 保存正确案例
    if key == ord("s"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(
            correct_dir,
            f"correct_{timestamp}.jpg"
        )

        cv2.imwrite(filename, annotated_frame)
        print(f"正确案例已保存：{filename}")

    # 保存错误案例
    elif key == ord("e"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(
            error_dir,
            f"error_{timestamp}.jpg"
        )

        cv2.imwrite(filename, annotated_frame)
        print(f"错误案例已保存：{filename}")

    # 退出
    elif key == ord("q"):
        print("程序退出")
        break

cap.release()
cv2.destroyAllWindows()
