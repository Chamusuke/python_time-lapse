from google.colab import drive
drive.mount('/content/drive')


mport matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import h5py
import cv2
import time

data = h5py.File('/content/drive/MyDrive/outdoor_day/outdoor_day2_data.hdf5')
images = data['davis']['left']['image_raw']
image_ts = data['davis']['left']['image_raw_ts']
image_raw_event_inds = data['davis']['left']['image_raw_event_inds']


plt.imshow(images[6000])


# 画像とタイムスタンプからタイムラプスを作成
# 動画の保存パスとファイル名
output_path = '/content/drive/MyDrive/event-based-cameraoutput.mp4'

# 動画のフレームレート（FPS）を設定
fps = 30

# 画像のサイズを取得
height, width = images.shape[1], images.shape[2]

def create_video_from_h5py(images, image_ts, output_path, fps=30):
    # 画像のサイズを取得
    height, width = images.shape[1], images.shape[2]

    # 動画の出力設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 最初のフレームのタイムスタンプを取得
    start_time = image_ts[0]

    # 画像とタイムスタンプの対応をループで処理
    print("動画変換中...")
    for i in range(len(images)):
        # タイムスタンプからフレームの時間を計算
        frame_time = (image_ts[i] - start_time) / 1000.0

        # 画像データを取得
        frame = images[i]

        # 画像をBGRからRGBに変換
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

        # 画像を動画に書き込む
        out.write(frame_rgb)

    # 動画ファイルをクローズしてリソースを解放
    out.release()
    print("動画変換完了")


if __name__ == '__main__':
    start = time.time()

    print("画像の総枚数{0}".format(len(images)))
    path = ('/content/drive/MyDrive/event-based-camera/video_1.mp4')
    create_video_from_h5py(images, image_ts, path)
    elapsed_time = time.time() - start
    print ("処理にかかった時間は:{0}".format(elapsed_time) + "[sec]")
