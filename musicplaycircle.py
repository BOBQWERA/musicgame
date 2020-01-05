import pygame
import time,os,random
import math
thisdir = 'c:/work/all/musicgame/' #自己改成当前文件夹路径

FILE={  #总访问路径
    'bgfile':thisdir+'/image/bg/',#背景图文件夹路径
    'playfile':'4',#这个就是当前文件夹下的子文件夹名称,里面存放音乐(支持.wav,.mp3),和谱面(支持.cir)文件
}


sqrt,power = math.sqrt,math.pow

size = [800,800]

simple = False #简单模式
AUTO = True #dalao模式

Quick = True #这玩意就是你嫌圆圈消失慢,有卡顿,就设成True

bg = True
bgcenter = False #True则是将图片中心放到背景上,False则是左上角
bgimgfiles = FILE['bgfile']+random.choice(os.listdir(FILE['bgfile']))
bgimg = pygame.image.load(bgimgfiles)
if bgcenter:
    bgrect = bgimg.get_rect()
    bgrect.center = (540,360)
else:
    bgrect = (0,0)

musicfile=None
txtfile=None
files = os.listdir(thisdir+FILE['playfile'])
for i in files:
    part=os.path.splitext(i)
    if len(part)!=2:continue
    if part[1] in ['.wav','.mp3']:musicfile = thisdir+FILE['playfile']+'/'+i
    if part[1] in ['.cir']:txtfile = thisdir+FILE['playfile']+'/'+i

if not musicfile or not txtfile:
    raise ValueError('你文件路径填错了,才..才不是本系统出错了呢,哼~')

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('music')


circlefilerange = [1,2,3] if not Quick else [5,6,7]

missedbefore = 1500
missedafter  = 2000
codes = ['bad','bad+','good','great','great+'][::-1]

pygame.mixer.music.load(musicfile)
clock = pygame.time.Clock()

def spesort(item):
    return item[1]
def loadrhythm():
    showlist = []
    with open(txtfile,'r',encoding='utf8') as f:
        for i in f.readlines(): #谱面数据
            i = i.strip().split(' ')
            speed = random.uniform(1.2,2)
            speed = 2
            i[1] = float(i[1])-speed
            if i[1]<0:
                speed = speed-i[1]
                i[1]=0
            i.append(speed)
            showlist.append(i)
    showlist.sort(key=spesort)
    return showlist

rhythmcircle = []
for i in circlefilerange:
    rhythmcircle.append([])
    imgfile = thisdir+'image/%d/'%i
    files = os.listdir(imgfile)
    for i in files:
        rhythmcircle[-1].append(pygame.image.load(imgfile+i).convert_alpha())

showlist = loadrhythm()

class Ways:
    def __init__(self):
        self.imglist = []
    def update(self):
        self.check()
        for index,i in enumerate(self.imglist):
            self.imglist[index]=i.update(time.time()) if type(i)==Imgs else i.update()
    def add(self,pos,center,speed,degree):
        i=Imgs(pos,center,speed,degree)
        self.imglist.append(i)
        if 15<=degree<30: pypresskeys['6'].append(i);pypresskeys['3'].append(i)
        elif 30<=degree<60: pypresskeys['3'].append(i)
        elif 60<=degree<75: pypresskeys['3'].append(i);pypresskeys['2'].append(i)
        elif 75<=degree<105: pypresskeys['2'].append(i)
        elif 105<=degree<120: pypresskeys['2'].append(i);pypresskeys['1'].append(i)
        elif 120<=degree<150: pypresskeys['1'].append(i)
        elif 150<=degree<165: pypresskeys['1'].append(i);pypresskeys['4'].append(i)
        elif 165<=degree<195: pypresskeys['4'].append(i)
        elif 195<=degree<210: pypresskeys['4'].append(i);pypresskeys['7'].append(i)
        elif 210<=degree<240: pypresskeys['7'].append(i)
        elif 240<=degree<255: pypresskeys['7'].append(i);pypresskeys['8'].append(i)
        elif 255<=degree<285: pypresskeys['8'].append(i)
        elif 285<=degree<300: pypresskeys['8'].append(i);pypresskeys['9'].append(i)
        elif 300<=degree<330: pypresskeys['9'].append(i)
        elif 330<=degree<345: pypresskeys['9'].append(i);pypresskeys['6'].append(i)
        else: pypresskeys['6'].append(i)

    def press(self,key):
        if not 257<=key<=265 or key==261: return
        key=str(key-256)
        if pypresskeys[key]:
            d=pypresskeys[key][0].distance()
            missed = missedafter if pypresskeys[key][0].outrange() else missedbefore
            if d<missed and not pypresskeys[key][0].pressed:
                showscore.add(codes[int(d//(missed/5))])
                pypresskeys[key][0].pressed=True
                combo.add()
    def check(self):
        for i in self.imglist[::-1]:
            if not i.alive:
                self.imglist.remove(i)
                if type(i)==Imgs:
                    degree=i.degree
                    if 15<=degree<30: pypresskeys['6'].remove(i);pypresskeys['3'].remove(i)
                    elif 30<=degree<60: pypresskeys['3'].remove(i)
                    elif 60<=degree<75: pypresskeys['3'].remove(i);pypresskeys['2'].remove(i)
                    elif 75<=degree<105: pypresskeys['2'].remove(i)
                    elif 105<=degree<120: pypresskeys['2'].remove(i);pypresskeys['1'].remove(i)
                    elif 120<=degree<150: pypresskeys['1'].remove(i)
                    elif 150<=degree<165: pypresskeys['1'].remove(i);pypresskeys['4'].remove(i)
                    elif 165<=degree<195: pypresskeys['4'].remove(i)
                    elif 195<=degree<210: pypresskeys['4'].remove(i);pypresskeys['7'].remove(i)
                    elif 210<=degree<240: pypresskeys['7'].remove(i)
                    elif 240<=degree<255: pypresskeys['7'].remove(i);pypresskeys['8'].remove(i)
                    elif 255<=degree<285: pypresskeys['8'].remove(i)
                    elif 285<=degree<300: pypresskeys['8'].remove(i);pypresskeys['9'].remove(i)
                    elif 300<=degree<330: pypresskeys['9'].remove(i)
                    elif 330<=degree<345: pypresskeys['9'].remove(i);pypresskeys['6'].remove(i)
                    else: pypresskeys['6'].remove(i)

numberlist = []
for i in list('0123456789'):
    numberlist.append(pygame.image.load(thisdir+'image/num/default-%s.png'%i))
class Combo3:
    def __init__(self,center,w,h):
        self.centers = [(center[0]-2*w,center[1]),(center[0]-w,center[1]),center]
        self.updating = [False,False,False]
        self.speed = 5
        self.center =center
        self.sufs = [pygame.Surface((w,h)).convert_alpha() for i in range(3)]
        self.combo = 0
        self.updatepool = [[],[],[]]
        self.string = '--0'
        self.weight = w
        self.height = h
        self.rect = pygame.Rect(0,0,w,h)
    def _to_string(self):
        return '-'*(3-len(str(self.combo)))+str(self.combo)
    def add(self):
        self.combo+=1
        string = self._to_string()
        old = '-' if self.string[2]=='-' else int(self.string[2])
        self.updatepool[2].append([int(string[2]),old,self.height])
        if self.combo%10 == 0 and self.combo>8:
            old = '-' if self.string[1]=='-' else int(self.string[1])
            self.updatepool[1].append([string[1],old,self.height])
        if self.combo%100 == 0 and self.combo>88:
            old = '-' if self.string[0]=='-' else int(self.string[0])
            self.updatepool[0].append([string[0],old,self.height])
        self.string = string
    def miss(self):
        self.combo=0
        self.string='--0'
    def update(self):
        for i in range(3):
            self.sufs[i].fill((0,0,0,0))
        if self.combo==0:return
        for i,j in enumerate(self.updatepool):
            if not j:
                self.updating[i]=False
                if self.string[i]!='-':
                    self.sufs[i].blit(numberlist[int(self.string[i])],(0,0))
                continue
            elif j and not self.updating[i]: self.updating[i] = True
            else:
                j[0][2]-=self.speed
                j[0][2] = j[0][2] if j[0][2]>=0 else 0
                new,old=j[0][:2]
                self.sufs[i].blit(numberlist[int(new)],(0,j[0][2]))
                if old!='-':
                    self.sufs[i].blit(numberlist[int(old)],(0,j[0][2]-self.height))
                if j[0][2]<=0:
                    self.updating[i]=False
                    self.updatepool[i].pop(0)
        for i in range(3):
            self.rect.center = self.centers[i]
            screen.blit(self.sufs[i],self.rect)

combo = Combo3((775,27),49,54)

class Showscore:
    def __init__(self):
        file = thisdir+'image/score/'
        self.score = {'miss':pygame.image.load(file+'0.png'),
                      'bad':pygame.image.load(file+'1.png'),
                      'bad+':pygame.image.load(file+'2.png'),
                      'good':pygame.image.load(file+'3.png'),
                      'great':pygame.image.load(file+'4.png'),
                      'great+':pygame.image.load(file+'5.png')

        }
        self.imglist = []
        self.max = 12
        self.rect = pygame.Rect(0,0,181,99)
        self.rect.center = (400,400)
    def add(self,code):
        self.imglist.append([self.score[code],0])
    def update(self):
        if self.imglist:
            screen.blit(self.imglist[0][0],self.rect)
            self.imglist[0][1] += 1
            if self.imglist[0][1]>=self.max:
                self.imglist.pop(0)
showscore = Showscore()

def mysort(item):
    return int(item[19:-4])
delist = []
imgfile = thisdir+'image/8/'
files = os.listdir(imgfile)
files.sort(key=mysort)
for i in files:
    delist.append(pygame.image.load(imgfile+i))
class Decorate:
    def __init__(self):
        self.count = 0
        self.max = len(delist)
        self.rect=delist[0].get_rect()
        self.rect.center=[400,400]
    def update(self):
        screen.blit(delist[self.count],self.rect)
        self.count = self.count+1 if self.count<len(delist)-1 else 0
decorate = Decorate()

def xor(a,b):
    if a and b or not a and not b: return False
    return True

class Imgs:
    def __init__(self,pos,center,speed,degree):
        self.starttime =time.time()
        self.imglist = random.choice(rhythmcircle)
        self.count = len(self.imglist)-1
        self.count = 0
        self.speed = speed
        self.center = center
        self.degree = degree
        self.max = len(self.imglist)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.minx = True if pos[0]<=self.center[0] else False
        self.miny = True if pos[1]<=self.center[1] else False
        self.pressed = False
        self.pos = pos
        self.finish = pos.copy()
    def distance(self):
        return power(self.finish[0]-self.center[0],2)+power(self.finish[1]-self.center[1],2)
    def outrange(self):
        return power(self.finish[0]-400,2)+power(self.finish[1]-400,2)>366*366
    def update(self,t):
        if not self.alive:return
        img = self.imglist[self.count]
        if self.count<10: self.count+=1
        if not self.pressed:
            posx = abs(self.center[0]-self.pos[0])*(t-self.starttime)/self.speed
            posy = abs(self.center[1]-self.pos[1])*(t-self.starttime)/self.speed
            if self.minx:
                x=self.pos[0]+posx
            else :
                x=self.pos[0]-posx
            posy = posy if self.miny else -posy
            y=self.pos[1]+posy
            self.finish = [x,y]
        else:
            x,y = self.finish
        d = power(x-self.center[0],2)+power(y-self.center[1],2)
        if d>=1000 and not self.pressed and power(x-400,2)+power(y-400,2)>366*366:
            way.imglist.append(Imgs2(self.center))
            showscore.add('miss')
            combo.miss()
            self.alive=False
            return self
        if self.pressed:
            self.count=self.count+1
        if self.count>=self.max-1:
            self.alive = False
        self.rect.center = (round(x),round(y))
        screen.blit(img,self.rect)
        return self

missdecircle = []
imgfile = thisdir+'image/4/'
files = os.listdir(imgfile)
for i in files:
    missdecircle.append(pygame.image.load(imgfile+i))

class Imgs2:
    def __init__(self,pos):
        self.imglist = missdecircle
        self.count = 0
        self.max = len(missdecircle)
        self.alive = True
        self.rect = self.imglist[0].get_rect()
        self.rect.center = pos
    def update(self):
        if not self.alive: return self
        img = self.imglist[self.count]
        screen.blit(img,self.rect)
        self.count+=1
        if self.count>=self.max-1:
            self.alive = False
        return self

pressdict = {'1':(202,247),
             '2':(247,292),
             '3':(292,337),
             '4':(157,202),
             '6':(337,382),
             '7':(112,157),
             '8':(67,112),
             '9':(22,67)
}

presssimpledict = {'1':225,
             '2':270,
             '3':315,
             '4':180,
             '6':0,
             '7':135,
             '8':90,
             '9':45
}

pypresskeys = {'1':[],'2':[],'3':[],'4':[],'6':[],'7':[],'8':[],'9':[]
}

def addshows():
    if showlist and time.time()-starttime>=showlist[0][1]:
        item = showlist.pop(0)
        if not simple:
            degree=random.randint(pressdict[item[0]][0],pressdict[item[0]][1])
        else:
            degree=presssimpledict[item[0]]
        degree = degree%360
        posX = 366*math.cos(math.radians(degree))+400
        posY = 366*math.sin(math.radians(degree))+400
        way.add([400,400],[posX,posY],item[2],degree)

def autopressed():
    for _,j in enumerate(list('12346789')):
        if not pypresskeys[j]:continue
        d = pypresskeys[j][0].distance()
        if d<=200:
            way.press(int(j)+256)

way = Ways()
fiximg = pygame.image.load(thisdir+'image/bigcircle.png')
rect = fiximg.get_rect()
rect.center = (400,400)
pygame.mixer.music.play(1,0)
starttime = time.time()
while True:
    screen.fill((0,0,0))
    if bg:
        screen.blit(bgimg,bgrect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            way.press(event.key)
    if AUTO: autopressed()
    screen.blit(fiximg,rect)
    decorate.update()
    addshows()
    way.update()
    showscore.update()
    combo.update()
    FPS = clock.tick(90) #修改帧数
    pygame.display.flip()