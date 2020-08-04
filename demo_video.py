from opencv_viewer.video_viewer import VideoViewer

if __name__ == '__main__':
    path = 'media/video/VID_20200629_123454.mp4'

    video_viewer = VideoViewer(path)
    video_viewer.vid_show()
