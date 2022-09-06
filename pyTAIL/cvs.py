import cv2
import numpy as np

import sys
import re
import os

from PIL import Image
from pathlib import Path

from .config import DIRPATH_OPENH264



class imgEditor():
    def __init__(self,parent_directory,imgext='jpg'):
        path = Path(parent_directory)

        paths = [p for p in path.glob(f'*.{imgext}')]
        if paths==[]:
            print('Not Found {} data'.format(imgext))
            sys.exit()

        sorter = [str(p.stem) for p in paths]
        paths = [p for _,p in sorted(zip(sorter,paths))]
        self.name = [p.stem for p in paths]
        
        print('imreading...')
        self.images = [cv2.imread(str(p)) for p in paths]
        shapes = [i.shape for i in self.images]
        shapes = np.vstack(shapes)
        if not np.all(np.all(shapes,axis=0)): 
            raise Exception('Including some different dimensions images')
        self.dim = shapes[0]
        print('end imread\n')


    def show(self,imgs=None):
        if imgs==None:
            imgs = self.images
        for im in imgs:
            cv2.imshow('color', im)
            cv2.waitKey(0)

    
    def save(self,save_directory,addname=None,basename=None,ext='jpg'):
        if not basename==None:
            basename = str(basename)
            self.name = [basename]*len(self.name)
        if not addname==None:
            addname = '_'+str(addname)
            self.name = [n+addname for n in self.name]

        ext = '.'+ext
        save = Path(save_directory)

        for name,im in zip(self.name,self.images):
            name += ext
            savepath = str(save/name)
            cv2.imwrite(savepath,im)


    def trim(self,w_bounds=None,h_bounds=None):
        """
        Trim specified dimentions.
        If a bounds attribute is None, self.dim will be assigned.

        w_bounds : (2,) float
            (start,end) - in {0,1}
        h_bounds : (2,) float
            (start,end) - in {0,1}

        """
        w_bounds,h_bounds = list(w_bounds),list(h_bounds)
        if w_bounds==None:
            w_bounds = (0,1)
        if h_bounds==None:
            h_bounds = (0,1)

        w_bounds[0] = int(self.dim[1]*w_bounds[0])
        w_bounds[1] = int(self.dim[1]*w_bounds[1])
        h_bounds[0] = int(self.dim[0]*h_bounds[0])
        h_bounds[1] = int(self.dim[0]*h_bounds[1])

        self.images = [im[h_bounds[0]:h_bounds[1],w_bounds[0]:w_bounds[1]]
            for im in self.images]
        


################################################################
################################################################
################################################################
################################################################
################################################################


class imgEncoder():
    def __init__(self,parent_directory,saveto_noext=None,ext='jpg'):
        if saveto_noext==None:
            self.save = parent_directory
        else:
            self.save = saveto_noext

        self.save = str(Path(self.save).resolve())
        path = Path(parent_directory)
        paths = [str(p) for p in path.glob(f'*.{ext}')]
        
        filenumber = [p.stem for p in path.glob(f'*.{ext}')]
        filenumber = [''.join(re.findall(r'\d+', n)) for n in filenumber]
        paths = [p for _,p in sorted(zip(filenumber,paths))]

        print('imreading......')
        self.images = [cv2.imread(p) for p in paths]
        
        print('end imread\n')

        baseShape = self.images[0].shape

        for index,img in enumerate(self.images[1:]):
            s = img.shape
            if not baseShape == s:
                print("All shapes of images are not equal")
                print("1st Image Shape:{}\n{}st Image Shape:{}".format(baseShape,index+2,s))
                sys.exit()


        self.size = (baseShape[1],baseShape[0])


    def _reshape(self,scale):
        if scale == 1:
            return (self.size,self.images)
        else:
            size = (int(self.size[0]*scale), int(self.size[1]*scale))
            return (size,[cv2.resize(img,size) for img in self.images])


    def mp4(self,frameRate=60,scale=1):
        savepath = self.save+".mp4"
        size, images = self._reshape(scale)

        print("mp4 run......")
        print("----image size:{}".format(size))
        print("----number of images:{}\n".format(len(images)))

        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        pwd = os.getcwd()
        os.chdir(DIRPATH_OPENH264)
        fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
        video = cv2.VideoWriter(savepath,fourcc,frameRate,size)

        if not video.isOpened():
            print("No images are opened")
            sys.exit()

        [video.write(img) for img in images]
        video.release()

        os.chdir(pwd)

        print('Finish Encoding')
        print(f'The video locaiton is {savepath}\n')


    def gif(self,
            frameRate=60,
            scale=1,
            n_loop=0,
            quantize=True,
            quantize_colors=256):
        """
        create gif animation from images.

        parameters
        --------
        frameRate int
          Indicate arbitary framerate.
          Perhaps gif animation is capable duration from 20[ms] to upper though.
        """

        savePath = self.save+".gif"
        size, images = self._reshape(scale)

        duration = int(1000/frameRate)

        print("gif run......")
        print("----image size:{}".format(size))
        print("----number of images:{}\n".format(len(images)))
        print("----original duration:{}\n".format(duration))

        if duration<20:
            print("duration is changed to 20[ms]")
            duration = 20

        video = [Image.fromarray(i) for i in images]
        if quantize:
            video = [i.quantize(colors=quantize_colors,method=0) for i in video]
        video[0].save(savePath,format='GIF', save_all=True, append_images=video[1:], optimize=False, loop=n_loop, duration=duration)

        print('Finish Encoding\n')


################################################################
################################################################
################################################################
################################################################
################################################################


class vidEncoder:
    def __init__(self,video_path,saveto_noext):
        self.cap = cv2.VideoCapture(video_path)
        self.save_to = Path(saveto_noext)

    def save_all_frames(self,
                        basename,
                        ext='jpg'):

        if not self.cap.isOpened():
            print('Failured to open video')
            return

        path = Path(self.dir_path)
        path.mkdir(exist_ok=True)
        base_path = path / basename

        n_frame = int(self.cap.get(cv2.self.cap_PROP_FRAME_COUNT))
        digit = len(str(n_frame))

        for i in range(n_frame):
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite('{}_{}.{}'.format(base_path, str(i).zfill(digit), ext), frame)
            else:
                return


################################################################
################################################################
################################################################
################################################################
################################################################


def h_concate_images(path1,
                     path2,
                     save_to,
                     readext='jpg',
                     saveext='jpg'):
    path1 = Path(path1)
    path2 = Path(path2)

    paths1 = [p for p in path1.glob(f'*.{readext}')]
    paths2 = [p for p in path2.glob(f'*.{readext}')]

    sorter1 = [str(p.stem) for p in paths1]
    paths1 = [p for _,p in sorted(zip(sorter1,paths1))]
    sorter2 = [str(p.stem) for p in paths2]
    paths2 = [p for _,p in sorted(zip(sorter2,paths2))]
    
    print('imreading1...')
    images1 = [cv2.imread(str(p)) for p in paths1]
    shapes = [i.shape for i in images1]
    shapes = np.vstack(shapes)
    if not np.all(np.all(shapes,axis=0)): 
        raise Exception('Including some different dimensions images')
    dim1 = shapes[0]
    print('end imread\n')

    print('imreading2...')
    images2 = [cv2.imread(str(p)) for p in paths2]
    shapes = [i.shape for i in images2]
    shapes = np.vstack(shapes)
    if not np.all(np.all(shapes,axis=0)): 
        raise Exception('Including some different dimensions images')
    dim2 = shapes[0]
    print('end imread\n')

    if dim1[0]!=dim2[0]: Exception('size v dont corresponds')

    len1,len2 = len(images1),len(images2)
    if len1>len2:
        diff = len1-len2
        images2 += [images2[-1]]*diff
    elif len2>len1:
        diff = len2-len1
        images1 += [images1[-1]]*diff

    merged = [cv2.hconcat([im1,im2]) for im1,im2 in zip(images1,images2)]

    save_to = Path(save_to).absolute()
    for i,im in enumerate(merged):
        name = f'hconcatenate_{i:05}.{saveext}'
        savepath = str(save_to/name)
        cv2.imwrite(savepath,im)
