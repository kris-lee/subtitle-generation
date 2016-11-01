# code for batch generating simple subtitle of TV players and Movies
# auth : Li zhichao
# data : 2016-11-1
# than : liuyuming for guiding entire process and Zhu hongji for providing myutil.py

# -*- coding:utf-8 -*-
import os,sys
import os,shutil
import PIL
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
import datetime
import myutils as mu
import traceback
import glob
import string
import cv2


##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def readmap(uri):
	fp = open(uri, "rb")
	chlist=[]
	for line in fp:
		line = line.rstrip()
		ch = line.split()[1]
		#print ch
		chlist.append(ch)

	fp.close()
	return chlist
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------




##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def readlist(wordlist):
	dic = []
	with open(wordlist,'r') as fobj:
		for eachLine in fobj:
			s = eachLine        
			dic.append(s.split('\n')[0])
	#print 'len(readlist):',len(dic)
	#print dic
	return dic
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------






##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def get_color():
	#ri = random.randint(0,len(colorlist)-1) 
	#ri = 4 balck font  ri = 0 white font
	ri = 4 
	return ri,colorlist[ri]
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------



##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def gen_str(dic):
	#str_len = random.randint(str_min, str_max) 
	strlist=random.choice(dic)
	#print "strlist: ",strlist
	#n_space = random.choice([""," ","  "])
	str = unicode(''.join(strlist),'utf-8')
	#print str
	return str
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------




##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def genImg(bgimg_path):

	global file_name
	global file_count

	imglist = mu.getImageListRecursive(bgimg_path)
	#imglist.sort(key = lambda x:int(x[:-4]))


	#print "chlist",chlist
	
	file_path = data_path + '/%d/' % file_name
	if not os.path.exists(file_path):
		os.makedirs(file_path)

	index = 0

	for abspath in imglist:
		imgID_str = os.path.basename(abspath).split('.')[0]
		imgID = string.atoi(imgID_str)

		
		dir_name = os.path.dirname(abspath)
		fileID_index = dir_name.rfind('/')
		fileID = dir_name[fileID_index + 1:]
		#print 'fileID: %s, imgID: %d'%(fileID, imgID)
	

		with open(abspath, 'rb') as fp:
			big_img = Image.open(fp)

			for (fonttype_key,fonttype_value) in fonttype.iteritems():

				
				fontfile = font_path + fonttype_key

				if True:
					index = index + 1	
					try:
						pasteWord(imglist, abspath, fileID, imgID, index, fonttype_value, fontfile, big_img)
					except Exception as err:
						print err
						traceback.print_exc()
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------




##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------
def pasteWord(imglist, abspath, fileID, imgID, index, fonttype_value, fontfile, big_img):

	global file_name
	global file_count
	global chlist
	## 0 get text
	#text = gen_str(chlist)

	## 1 cut background
	img_width, img_height = big_img.size
	im = big_img.copy()
	draw = ImageDraw.Draw(im)
	font_total_len = float("inf")

	#sh_shift = random.randint(1, 1)
	
	while  (img_width - font_total_len < (10 + sh_shift)) : 
		text = gen_str(chlist)
		font_distance = random.randint(font_distance_min, font_distance_max)
		font_size = random.randint(font_size_min, font_size_max)
		font_total_len = font_size * len(text) + font_distance * (len(text) -1 )

	
	## 2 font distance


	## 3 font color
	color_id = 0
	color_id, color = get_color()



	## 4 font type
	font_white = ImageFont.truetype(fontfile, font_size)
	font_black = ImageFont.truetype(fontfile, font_size)



	## 5 font start position
	font_start_posx = random.randint(0 + sh_shift, img_width - font_total_len - sh_shift)
	font_start_posy = random.randint(0 + sh_shift, img_height - font_size - 10 - sh_shift)


	
	## 6 ROI
	if fonttype_value == "lvshu":
		upper_left_posy = font_start_posy + int(font_size / 6)
		lower_right_posy = font_start_posy + font_size - int(font_size / 10)
	else:

		upper_left_posy = font_start_posy
		lower_right_posy = font_start_posy + font_size

	ROI_upper_left_posx = font_start_posx - sh_shift
	ROI_upper_left_posy = upper_left_posy - sh_shift
	ROI_lower_right_posx = font_start_posx + font_total_len + sh_shift
	ROI_lower_right_posy = lower_right_posy + sh_shift	

	ROI_upper_left_point = "%d,%d" % (ROI_upper_left_posx, ROI_upper_left_posy)
	ROI_lower_right_point = "%d,%d" % (ROI_lower_right_posx, ROI_lower_right_posy)
	
	ROI_point = "%s;%s" % (ROI_upper_left_point, ROI_lower_right_point)



	## 7 draw text outline & shadow
	font_posx = font_start_posx
	font_posy = font_start_posy

	white_RGB = random.randint(0, 100)
	bs_color =  (white_RGB, white_RGB, white_RGB)


	for key in text:
		draw.text((font_posx - sh_shift, font_posy - sh_shift), key, bs_color, font = font_black)
		draw.text((font_posx - sh_shift, font_posy), key, bs_color, font = font_black)
		draw.text((font_posx - sh_shift, font_posy + sh_shift), key, bs_color, font = font_black)

		draw.text((font_posx, font_posy - sh_shift), key, bs_color, font = font_black)
		draw.text((font_posx, font_posy + sh_shift), key, bs_color, font = font_black)

		draw.text((font_posx + sh_shift, font_posy - sh_shift), key, bs_color, font = font_black)
		draw.text((font_posx + sh_shift, font_posy), key, bs_color, font = font_black)
		draw.text((font_posx + sh_shift, font_posy + sh_shift), key, bs_color, font = font_black)


		draw.text((font_posx, font_posy), key, ws_color, font = font_white)
		font_posx = font_posx +  font_size + font_distance


	jpg_name =  "file%s_bg%010d_%010d_%s_size%02d_dis%02d.jpg" % (fileID, imgID, index, fonttype_value, font_size, font_distance)


	file_path = data_path + '/%s/' % file_name
	res_uri = file_path + '/%s' % jpg_name	
	im.save(res_uri)
	
	id2textmap.append((jpg_name, ROI_point, text.encode('utf-8')))
	textsum.append((jpg_name, ROI_point, text.encode('utf-8')))
	
	file_count = file_count + 1
	
	if file_count == 14000 :
	
		file_count = 0

		text_name = file_path + 'list_%s.txt' % file_name
		with open(text_name, "wb") as tn:
			for tu in id2textmap:
				line = '%s %s %s\n'%(tu[0],tu[1],tu[2])
				tn.write(line)
		
		del id2textmap[:]


		file_name = file_name + 1
		 
		file_path = data_path + '/%d/' % file_name
		if not os.path.exists(file_path):
			os.makedirs(file_path)
	
##------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------




    
if __name__ == '__main__':

	phase = sys.argv[1]
	if phase == 'train':
		data_path = '/N2N_OCR/test/train5m_4color_7font_shadow'
	elif phase == 'val': 
		data_path = '/data/Subtitle/Subtitle_Edge/'

	##path parameter
	bgimg_path='/home/lizhichao/data/Subtitle/Background_Image/'
	font_path = '/home/lizhichao/data/Subtitle/Font/'

	##image size parameter
	image_width = 32
	image_height = 32
	

	global file_name
	global file_count
	file_name = 0
	file_count = 0


	##str parameter
	str_min = 4
	str_max = 15

     
	##fonttype parameter	
	fonttype = {'simfang.ttf':'fangsong', 'STXINGKA.TTF':'huawen_xingkai', 'simkai.ttf':'kaiti',\
	 'STXINWEI.TTF':'huawen_xinwei', 'simsun.ttc':'songti', 'SIMLI.TTF':'lvshu', 'simhei.ttf':'heiti'}
	fonttype_num = len(fonttype)	
	
  
	#fontsize parameter 
	font_size_min = 30 
	font_size_max = 90
	font_size = random.randint(font_size_min, font_size_max)


	##fontdistance parameter
	font_distance_min = 0
	font_distance_max = 10
	font_distance = random.randint(font_distance_min, font_distance_max)


	## gen number of items per bgimg
	global id2textmap
	global textsum
	global chlist
	chlist = readlist('/data/Subtitle/large_word_1000w.txt')
	id2textmap = []
	textsum = []


	## shadow color paramter
	shift_min = 1
	shift_max = 5
	sh_shift = random.randint(shift_min, shift_max)


	#bs_color = (100,100,100) # black shadow
	ws_color = (0xf0,0xf0,0xf0) # white shadow


	colorlist=[(0xff,0xff,0xff),(0xff,0,0),(0x00,0xff,0x00),(0x00,0x00,0xff),(0x00,0x00,0x00)]


	tm_start = datetime.datetime.now()
	mu.mkdir(data_path)

	
	#global id2textmap

	## do 
	genImg(bgimg_path)

	text_total = data_path + 'list_sum.txt'
	with open(text_total, "wb") as tt:
		for ts in textsum:
			line = '%s %s %s\n'%(ts[0],ts[1],ts[2])
			tt.write(line)
	del textsum[:]
