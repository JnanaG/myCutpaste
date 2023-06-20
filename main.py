import random
from PIL import Image, ImageFilter
import os


def convert_to_yolo_format(paste_position, image, composite):
    x, y = paste_position
    potx, poty = x+image.width/2, y+image.height/2
    yolox, yoloy, yolow, yoloh = potx/composite.width, poty/composite.height, image.width/composite.width, image.height/composite.height
    return yolox, yoloy, yolow, yoloh


def check_intersection(position, image, paste_positions):

    x1, y1 = position
    width1, height1 = image.size

    for paste_position, paste_size in paste_positions:
        x2, y2 = paste_position
        width2, height2 = paste_size

        if x1 < x2 + width2 and x1 + width1 > x2 and y1 < y2 + height2 and y1 + height1 > y2:
            return True
    return False


def cutpaste(template, image_filenames, num_patchs):
    paste_positions = []
    composite = template
    label_dict = {'A_offset': 0, 'B_missing_part': 1, 'C_libei': 2}
    num_patchs = random.randint(6, 10)
    selected_images = random.sample(image_filenames, num_patchs)
    paste_position = None
    yolo_txt = []
    for cutout in selected_images:
        patch = Image.open(cutout)
        patch = patch.filter(ImageFilter.MedianFilter(size=3))
        patch = patch.resize((patch.size[0]//2, patch.size[1]//2))

        while paste_position is None or check_intersection(paste_position, patch, paste_positions):
            # print(paste_position)
            paste_position = (random.randint(0, composite.width - patch.width), random.randint(0, composite.height - patch.height))
        
        yolox, yoloy, yolow, yoloh = convert_to_yolo_format(paste_position, patch, composite)
        label = label_dict[cutout.split('/')[-2]]
        yolo_line = label, yolox, yoloy, yolow, yoloh
        yolo_txt.append(yolo_line)
        composite.paste(patch, paste_position)
        paste_positions.append((paste_position, patch.size))
    
    normalcutouts = []
    for Z_normal in os.listdir('Z_normal'):
        Z_normal_path = os.path.join('Z_normal', Z_normal)
        normalcutouts.append(Z_normal_path)
    num_normal = random.randint(2, 5)
    print('num_patchs, num_normal: ', num_patchs, num_normal)
    normalcut_images = random.sample(normalcutouts, num_normal)
    for normalcut in normalcut_images:
        patch = Image.open(normalcut)
        patch = patch.filter(ImageFilter.MedianFilter(size=3))
        patch = patch.resize((patch.size[0]//2, patch.size[1]//2))

        while paste_position is None or check_intersection(paste_position, patch, paste_positions):
            paste_position = (random.randint(0, composite.width - patch.width), random.randint(0, composite.height - patch.height))
        composite.paste(patch, paste_position)
        paste_positions.append((paste_position, patch.size))
        
    return composite, yolo_txt

def main(template, patch_path):
    template = Image.open(template)

    path = patch_path
    image_filenames = []
    for subdir in os.listdir(path):
        subdir_path = os.path.join(path, subdir)
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            image_filenames.append(file_path)

    composite, yolo_txt = cutpaste(template, image_filenames, 8)
    # composite.save('result1.jpg')
    return composite, yolo_txt

if __name__ == '__main__':
    template = 'template.jpg'
    patch_path = 'lianbao3f'
    for iter in range(10000):
        composite, yolo_txt = main(template, patch_path)
        composite.save(f'generation/res{iter}.jpg')

        with open(f'glabel/res{iter}.txt', 'w')as f:
            for i in range(len(yolo_txt)):
                line = f"{yolo_txt[i][0]} {yolo_txt[i][1]} {yolo_txt[i][2]} {yolo_txt[i][3]} {yolo_txt[i][4]}\n"
                f.write(line)

