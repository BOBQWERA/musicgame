import pygame
import time,os

#写谱的工具
#做好谱子后连同音乐放到当前文件夹下的新建子文件夹下(需要手动)

size = [800,800]

pygame.init()

thisdir='c:/work/all/mm/'
musicfile=thisdir+'4/world.mp3' #音乐路径

class Showcommand:
    def __init__(self):
        self.imglist = []
    def update(self):
        for i in self.imglist:
            i.update()
    def add(self,key):
        if 257<=key<=265 and key!=261:
            pos = centers[key-257] if key<261 else centers[key-258]
            keystring = str(key-256)
            self.imglist.append(Imgs(list(pos)))
            commands.append([keystring,str(round(time.time()-starttime,3))])

L = []
imgfile = thisdir+'image/4/'
files = os.listdir(imgfile)
for i in files:
    L.append(pygame.image.load(imgfile+i))

class Imgs:
    def __init__(self,pos):
        self.imglist = L
        self.count = 0
        self.max = len(L)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.rect.center = pos
    def update(self):
        if not self.alive: return
        img = self.imglist[self.count]
        screen.blit(img,self.rect)
        self.count+=1
        if self.count>=self.max-1:
            self.alive = False

screen = pygame.display.set_mode(size)
pygame.display.set_caption('music')

pygame.mixer.music.load(musicfile)

clock = pygame.time.Clock()

fiximg = pygame.image.load(thisdir+'image/approachcircle.png')
rect = pygame.Rect(0,0,250,253)
centers = [(j*250+150,(2-i)*250+150) for i in range(3) for j in range(3)]
centers.pop(4)

commands = []
show = Showcommand()

pygame.mixer.music.play(1,0)
starttime = time.time()

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open(thisdir+'data3.cir','w',encoding='utf8') as f: #谱面数据储存路径
                for i in commands:
                    f.write(i[0]+' '+i[1]+'\n')
            exit()
        elif event.type == pygame.KEYDOWN:
            show.add(event.key)
    for i in range(8):
        rect.center=centers[i]
        screen.blit(fiximg,rect)
    show.update()
    pygame.display.flip()
