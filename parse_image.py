from __future__ import division

try:
    import cPickle as pickle
except ImportError:
    import pickle
import PIL.Image as image

"""总结一下：最终的图片就是把拼图，
按照x=66、y=40、w=22、h=58截取出来，放在上半部分第一个位置
，x= 286、y=40、w=22、h=58截取出来放在上半部分第二个位置，紧挨着第一个，以此类推，拼成一张整图。"""
a = [{'y': 40, 'x': 66},
     {'y': 40, 'x': 286},
     {'y': 98, 'x': 66},
     {'y': 40, 'x': 44},
     {'y': 40, 'x': 154},
     {'y': 40, 'x': 22},
     {'y': 98, 'x': 88},
     {'y': 40, 'x': 198},
     {'y': 98, 'x': 198},
     {'y': 98, 'x': 264},
     {'y': 40, 'x': 308},
     {'y': 40, 'x': 176},
     {'y': 98, 'x': 0},
     {'y': 98, 'x': 132},
     {'y': 40, 'x': 132},

     {'y': 98, 'x': 176},
     {'y': 40, 'x': 88},
     {'y': 98, 'x': 154},
     {'y': 40, 'x': 220},
     {'y': 40, 'x': 264},
     {'y': 40, 'x': 110},
     {'y': 98, 'x': 242},
     {'y': 98, 'x': 286},
     {'y': 40, 'x': 0},
     {'y': 40, 'x': 242},
     {'y': 98, 'x': 44},
     {'y': 98, 'x': 220},
     {'y': 98, 'x': 22},
     {'y': 98, 'x': 308},
     {'y': 98, 'x': 110},

     {'y': 0, 'x': 264},
     {'y': 0, 'x': 154},
     {'y': 0, 'x': 44},
     {'y': 0, 'x': 242},
     {'y': 0, 'x': 110},
     {'y': 0, 'x': 176},
     {'y': 0, 'x': 88}
     ]


def get_merge_image(filename, location_list):
    im = image.open(filename)
    im_list_upper = []
    im_list_down = []
    im_list_xiao = []
    for location in location_list[:15]:
        im_list_upper.append(im.crop((
            abs(location['x']), abs(location['y']),
            abs(location['x'])+21.98, abs(location['y']) + 58+58)))
    for location in location_list[15:]:
        im_list_down.append(im.crop((
            abs(location['x']), abs(location['y']),
            abs(location['x'])+21.98, abs(location['y']) + 58)))
    for location in location_list:
        if location['y'] == 0:
            im_list_xiao.append(im.crop((
                abs(location['x']), 0,
                abs(location['x']) + 22, 0 + 40)))

    # 画布
    new_im = image.new('RGB', (15 * 22, 50 + 58 * 2))
    # 小图片拼接
    x_offset = 175
    for im in im_list_xiao:
        new_im.paste(im, (x_offset, 5))  # 将im 粘贴到new_im 位置(x_offset,80)
        x_offset += im.size[0]

    # 上部分拼接
    x_offset = 0
    for im in im_list_upper:
        new_im.paste(im, (x_offset, 50))
        x_offset += im.size[0]

    # 下部分拼接
    x_offset = 0
    for im in im_list_down:
        new_im.paste(im, (x_offset, 50 + 58))  # 将im 粘贴到new_im 位置(x_offset,80)
        x_offset += im.size[0]

    return new_im


def get_new_image():
    # 合并图片使用
    new_image1 = get_merge_image(filename='full.jpg', location_list=a)
    new_image1.save('image1.jpg')


if __name__ == '__main__':
    get_new_image()
    # print(a[:16])
