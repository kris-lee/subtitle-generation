


# -*- coding:utf-8 -*-
import os
import json
import sys
import os,shutil
from PIL import Image, ImageDraw


def get_information(txt_list_path):
	txt_list = []
	for root, dir, files in os.walk(txt_list_path):
		for txt_name in files:
			filename = os.path.join(root, txt_name)
			txt_list.append(filename)
	
	fp = open(fail_save_path, 'wb')
	np = open(no_save_path, 'wb')
	op = open(one_save_path, 'wb')
	mp = open(more_save_path, 'wb')

	for filename in txt_list:
		lines = open(filename, 'rb').readlines()
		for line in lines:
			len_split = len(line.split())
			# 判断line是否为空的
			if len_split == 0:
				print 'line is null\n'
				continue
			abspath = line.split()[0]
			img_ID = abspath[abspath.rfind('/')+1:]
			label_line = line[len(line.split()[0]):]
			# 未识别的标签为 “<!DOCTYPE html>”
			if 'html' in label_line:
				print 'new_line: %s......subtitle fail recognize\n' % img_ID
				fail_img_name = '%s\n' % img_ID
				fp.write(fail_img_name)
				continue
			# 调用json，转换到python的字典形式
			json_line = json.loads(label_line)
			ret_info = json_line.get('ret', 'None')
			rect_with_word_sum = ''
			# 图片能够识别出来，并且图片中没有字符
			if ret_info == 'None' or len(ret_info) == 0:
				print 'new_line: %s......no subtitle\n' % img_ID
				no_img_name = '%s\n' % img_ID
				np.write(no_img_name)
				continue
			# 判断line识别出多少组字符
			for ret_info_ID in range(len(ret_info)):
				pos = ret_info[ret_info_ID]['rect']
				print 'pos:%s' % pos
				left_top_pos = '%s,%s' % (pos['left'],pos['top'])
				right_bottom_pos = '%d,%d' % (int(pos['left'])+int(pos['width']), int(pos['top'])+int(pos['height']))
				roi_pos = '[%s,%s]' % (left_top_pos, right_bottom_pos)
				print 'roi_pos:%s' % roi_pos
				word = ret_info[ret_info_ID]['word']
				rect_with_word = ' %s %s' % (roi_pos, word)
				if ret_info_ID > 0:
					rect_with_word = ' ;' + rect_with_word
				rect_with_word_sum = rect_with_word_sum + rect_with_word
			new_line = '%s%s\n' % (img_ID, rect_with_word_sum.encode('utf-8'))
			print 'new_line: %s' % new_line
			# 图片能够识别出来，并且图片中只有一组字符
			if len(ret_info) == 1:
				op.write(new_line) 
			# 图片能够识别出来，并且图片中有多于一组的字符
			else:
				mp.write(new_line)	
	
	np.close()
	op.close()
	mp.close()


if __name__ == '__main__':
	txt_list_path = '/data/baidu_subtitle_txt_list/'
	# 1、未能识别的图片list
	fail_save_path = '/data/baidu_information_fail_subtitle.txt' 
	# 2、能识别并且没有字符的图片list
	no_save_path = '/data/baidu_information_no_subtitle.txt'
	# 3、能识别并且只有一组字符的图片list
	one_save_path = '/baidu_information_one_subtitle.txt'
	# 4、能识别并且多于一组字符的图片list
	more_save_path = '/data/baidu_information_more_subtitle.txt'
	
	get_information(txt_list_path)

