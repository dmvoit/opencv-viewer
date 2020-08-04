from opencv_viewer.img_viewer import Viewer

if __name__ == '__main__':
    path = 'media/photo'

    viewer = Viewer(path)
    viewer.img_show()
