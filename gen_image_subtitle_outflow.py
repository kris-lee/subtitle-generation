# code for batch generating simple outflow subtitle of TV players and Movies
# auth : Li zhichao
# data : 2016-11-1
# than : Liu yuming for guiding entire process, He neng for providing approach to generate outflow and Zhu hongji for providing myutil.py


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
import cv2.cv as cv
import cv2
import math
import numpy

##----------------------------------------------------------------------------------------------------------
##----------------------------------------------------------------------------------------------------------

def readlist(wordlist):
        dic = []
        with open(wordlist,'r') as fobj:
                for eachLine in fobj:
                        s = eachLine
                        dic.append(s.split('\n')[0])
        return dic



def gen_str(dic):
        strlist=random.choice(dic)
        str = unicode(''.join(strlist),'utf-8')
        return str



def get_font(color):
	fonttype = {'simfang.ttf':'fangsong', 'STXINGKA.TTF':'huawen_xingkai', 'simkai.ttf':'kaiti',\
         'STXINWEI.TTF':'huawen_xinwei', 'simsun.ttc':'songti', 'SIMLI.TTF':'lvshu', 'simhei.ttf':'heiti'}
	
	#fontfile = font_path + random.choice(fonttype.keys())
	fontfile = font_path + 'simhei.ttf'

	colorlist=[(0xff,0,0),(0x00,0xff,0x00),(0x00,0x00,0xff),(0xff,0xff,0xff),(0x00,0x00,0x00)]
	
	#font_color = random.choice(colorlist)
	font_color = colorlist[color]

	return fontfile, font_color



def text_record(img_width):
	global chlist
	font_total_len = float("inf")

	while  (img_width - font_total_len < (blur_width * 3)):
		text = gen_str(chlist)
		font_distance = random.randint(font_distance_min, font_distance_max)
		font_size = random.randint(font_size_min, font_size_max)
		#font_size = 86
		font_total_len = font_size * len(text) + font_distance * (len(text) -1 )

	return text, font_distance, font_size, font_total_len



def text_start_point(img_width, img_height, font_size, font_total_len):
	leftupper_posX = random.randint(0, img_width - font_total_len - blur_width*3)
        leftupper_posY = random.randint(0, img_height - font_size - blur_width*3)
	
	return leftupper_posX, leftupper_posY



def draw_text(img_bg, posX, posY, text, font_distance, font_size, font_total_len, color):	
	font_type, font_color = get_font(color)
	font =  ImageFont.truetype(font_type, font_size)
	
	draw = ImageDraw.Draw(img_bg)

	for key in text:
                draw.text((posX, posY), key, font_color, font = font)
                posX = font_distance + font_size + posX

	return img_bg



def get_ROI(start_posX, start_posY, font_size, font_total_len, blur_width):
	
	end_posX = start_posX + font_total_len + blur_width*2
	end_posY = start_posY + font_size + blur_width*2

	ROI_upper_left_point = "%d,%d" % (start_posX, start_posY)
	ROI_lower_right_point = "%d,%d" % (end_posX, end_posY)
	
	ROI_point = "%s;%s" % (ROI_upper_left_point, ROI_lower_right_point)
	return ROI_point




def generate_jpg_name(abspath, text_count, font_size, font_distance):
	#jpg name
	imgID_str = os.path.basename(abspath).split('.')[0]
	imgID = string.atoi(imgID_str)
	dir_name = os.path.dirname(abspath)
	fileID_index = dir_name.rfind('/')
	fileID = dir_name[fileID_index + 1:]
	jpg_name = "file%s_bg%010d_%010d_%s_size%02d_dis%02d.jpg" % (fileID, imgID, text_count, 'heiti', font_size, font_distance)

	return jpg_name

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

def generate_file(result_img, jpg_name, text, ROI_point):
	
        global file_name
        global file_count
	
	file_path = saveimg_path + '/%s/' % file_name
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	result_path = file_path + '/%s' % jpg_name
	result_img.save(result_path)

	textpart.append((jpg_name, ROI_point, text.encode('utf-8')))
	textsum.append((jpg_name, ROI_point, text.encode('utf-8')))

	file_count = file_count + 1

	if file_count == 30 :

		file_count = 0

		text_name = file_path + 'list_%s.txt' % file_name
		with open(text_name, "wb") as tn:
			for tu in textpart:
				line = '%s %s %s\n'%(tu[0],tu[1],tu[2])
				tn.write(line)

		del textpart[:]

		file_name = file_name + 1

		file_path = saveimg_path + '/%d/' % file_name
		if not os.path.exists(file_path):
			os.makedirs(file_path)

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------




#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

def procedure(abspath, text_count):

	img_bg = cv2.imread(abspath)
	img_width = img_bg.shape[1]	
	text, font_distance, font_size, font_total_len = text_record(img_width)
	bg_width = font_total_len + blur_width * 2
	bg_height = font_size + blur_width*2
	white_bg = Image.new("RGB",[bg_width, bg_height], 'white')
	posX = blur_width
	posY = blur_width

	
	color = 0 #red color
	#color = 4 #black color
	white_bg = draw_text(white_bg, posX, posY, text, font_distance, font_size, font_total_len, color)


	#PIL convert to Opencv
	Opencv_Origin_img = numpy.array(white_bg)	
	#Opencv Outflow
	Opencv_outflow_img = generate_outerflow(Opencv_Origin_img, text_count, font_size)
	#print opencv_outflow_img to img_bg
	outflowtextimg, posX, posY = get_glowimg(img_bg, Opencv_outflow_img, text_count)


	ROI_point = get_ROI(posX, posY, font_size, font_total_len, blur_width)
	jpg_name = generate_jpg_name(abspath, text_count, font_size, font_distance)

	PIL_outflow_img = Image.open(outflowtextimg)
	color = 3 # white color
	posX = blur_width + posX
	posY = blur_width + posY
	result_img = draw_text(PIL_outflow_img, posX, posY, text, font_distance, font_size, font_total_len, color)
	
	generate_file(result_img, jpg_name, text, ROI_point)



def generate_outerflow(Opencv_Origin_img, text_count, font_size):
	
	Opencv_Origin_img = cv2.cvtColor(Opencv_Origin_img, cv2.COLOR_RGB2BGR)

	if font_size < 55:
		scale = font_size/5
	elif 54 < font_size < 85:
		scale = font_size/5 -2
	else:
		scale = 13
	if scale%2 == 0:
		scale = scale - 1
	ksize = (scale, scale)

	# erode
	kernel = numpy.ones(ksize, numpy.uint8)
	iteration = 1
	erode_white_bg = cv2.erode(Opencv_Origin_img, kernel, iteration)
	
	#Gaussian blur
	sigmoidX = 0
	gaussianblur_white_bg = erode_white_bg
	gaussianblur_white_bg = cv2.GaussianBlur(gaussianblur_white_bg, (scale+2, scale+2), sigmoidX)
	gaussianblur_white_bg = cv2.GaussianBlur(gaussianblur_white_bg, ksize, sigmoidX)

	return gaussianblur_white_bg

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

def get_glowimg(img1, img2, text_count):
		 
	img2_height, img2_width, img2_channel = img2.shape
	img1_height, img1_width, img1_channel = img1.shape

	start_posx = random.randint(0, img1_width - img2_width)
	start_posy = random.randint(0, img1_height - img2_height)
	
	roi = img1[start_posy : start_posy + img2_height, start_posx : start_posx + img2_width] 
	
	# Now create a mask of logo and create its inverse mask also
	img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)	

	ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)

	mask_inv = cv2.bitwise_not(mask)
 
	# Now white-out the area of logo in ROI
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask)

	# Take only region of logo from logo image.
	img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)
	 
	# Put logo in ROI and modify the main image
	dst = cv2.add(img1_bg,img2_fg)

	img1[start_posy : start_posy + img2_height, start_posx : start_posx + img2_width] = dst
	outflowtextimg = outflowimg_path+ '%d.jpg' % text_count
	cv2.imwrite(outflowtextimg, img1)

	return outflowtextimg, start_posx, start_posy

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
	



#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
def generate_result(bgimg_path):

	imglist = mu.getImageListRecursive(bgimg_path)
	text_count = 0

	for abspath in imglist:
		# load background image
		procedure(abspath, text_count)
		text_count = text_count + 1

	text_total = saveimg_path + 'list_sum.txt'
	with open(text_total, "wb") as tt:
		for ts in textsum:
			line = '%s %s %s\n'%(ts[0],ts[1],ts[2])
			tt.write(line)
	del textsum[:]

#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------




if __name__ == '__main__':
	bath_path = '/home/lizhichao/data/Subtitle/'
	bgimg_path = bath_path + 'Sample/'
	saveimg_path = bath_path + 'Sample_Test/'

	origintext_path = bath_path + 'OriginText/'
	erodetext_path = bath_path + 'ErodeText/'
	gaussianblurtext_path = bath_path + 'GaussianBlurText/'
	graytext_path = bath_path + 'GrayText/'
	outflowimg_path = bath_path + 'Sample_OutflowText/'
	masktextimg_path = bath_path + 'MaskTest/'

	textimg_path = bath_path + 'Text_Img/'
	font_path = bath_path + 'Font/'

	if os.path.exists(saveimg_path):
		shutil.rmtree(saveimg_path)
	os.mkdir(saveimg_path)

	if os.path.exists(outflowimg_path):
		shutil.rmtree(outflowimg_path)
	os.mkdir(outflowimg_path)


	global chlist	
	global file_name
	global file_count
	global textpart
	global textsum
	chlist = readlist(bath_path + 'sample_list_lowfrequent.txt')
	file_name = 0
	file_count = 0
	textpart = []
	textsum = []



	font_distance_min = 0
	font_distance_max = 10
	font_size_min = 30
	font_size_max = 90

	blur_width = 5
	generate_result(bgimg_path)	
