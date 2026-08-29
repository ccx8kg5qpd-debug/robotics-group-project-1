import cv2
import time
import json
import os
from datetime import datetime
from collections import deque

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from ultralytics import YOLO


class YoloDetectionNode(Node):

    def __init__(self):
        super().__init__("qyy_yolo_detector")

        # ROS2 Publisher
        self.publisher = self.create_publisher(
            String,
            "/qyy/detections",
            10
        )

        # 加载自己训练的模型
        self.model = YOLO("best.pt")

        # 摄像头
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise RuntimeError("无法打开摄像头")

        # FPS统计
        self.frame_times = deque(maxlen=30)

        # 保存结果的目录
        self.correct_dir = "results/correct_cases"
        self.error_dir = "results/error_cases"

        os.makedirs(self.correct_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)

        self.get_logger().info("QYY YOLO ROS2 node started")
        self.get_logger().info("Publishing topic: /qyy/detections")
        self.get_logger().info("S = save correct case")
        self.get_logger().info("E = save error case")
        self.get_logger().info("Q = quit")

    def run(self):

        while rclpy.ok():

            start_time = time.time()

            ret, frame = self.cap.read()

            if not ret:
                self.get_logger().error("无法读取摄像头")
                break

            # YOLO推理
            results = self.model.predict(
                frame,
                conf=0.70,
                device=0,
                verbose=False
            )

            result = results[0]

            # 绘制检测框
            annotated_frame = result.plot()

            # --------------------------------
            # FPS
            # --------------------------------

            frame_time = time.time() - start_time
            self.frame_times.append(frame_time)

            avg_time = sum(self.frame_times) / len(self.frame_times)
            fps = 1.0 / avg_time

            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.1f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # --------------------------------
            # 提取YOLO检测结果
            # --------------------------------

            detections = []

            if result.boxes is not None:

                for box in result.boxes:

                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])

                    class_name = self.model.names[class_id]

                    x1, y1, x2, y2 = (
                        box.xyxy[0]
                        .cpu()
                        .numpy()
                        .astype(int)
                        .tolist()
                    )

                    detection = {
                        "class": class_name,
                        "confidence": round(confidence, 3),
                        "bbox": [
                            int(x1),
                            int(y1),
                            int(x2),
                            int(y2)
                        ]
                    }

                    detections.append(detection)

            # --------------------------------
            # ROS2发布
            # --------------------------------

            message_data = {
                "fps": round(fps, 1),
                "detections": detections
            }

            msg = String()

            msg.data = json.dumps(
                message_data,
                ensure_ascii=False
            )

            self.publisher.publish(msg)

            # --------------------------------
            # 屏幕提示
            # --------------------------------

            cv2.putText(
                annotated_frame,
                "S: Correct | E: Error | Q: Quit",
                (20, annotated_frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                "QYY YOLO + ROS2 Detection",
                annotated_frame
            )

            key = cv2.waitKey(1) & 0xFF

            # 保存正确案例
            if key == ord("s"):

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S_%f"
                )

                filename = os.path.join(
                    self.correct_dir,
                    f"correct_{timestamp}.jpg"
                )

                cv2.imwrite(
                    filename,
                    annotated_frame
                )

                print(
                    f"正确案例已保存: {filename}"
                )

            # 保存错误案例
            elif key == ord("e"):

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S_%f"
                )

                filename = os.path.join(
                    self.error_dir,
                    f"error_{timestamp}.jpg"
                )

                cv2.imwrite(
                    filename,
                    annotated_frame
                )

                print(
                    f"错误案例已保存: {filename}"
                )

            # 退出
            elif key == ord("q"):
                break

            # ROS2处理内部事件
            rclpy.spin_once(
                self,
                timeout_sec=0
            )

        self.cap.release()
        cv2.destroyAllWindows()


def main():

    rclpy.init()

    node = YoloDetectionNode()

    try:
        node.run()

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
