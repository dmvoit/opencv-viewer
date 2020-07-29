from opencv_viewer.img_viewer import Viewer
from opencv_viewer.video_viewer import VideoViewer

video = True

if __name__ == '__main__':
    if video:
        path = 'media/video/'

        video_viewer = VideoViewer(path)
        video_viewer.vid_show()
    else:
        path = 'media/photo'

        viewer = Viewer(path)
        viewer.img_show()
