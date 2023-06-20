import random

from PIL import Image

# 打开源图像和目标图像
source_image = Image.open('test1332.jpg')
target_image = Image.open('template-11.jpg')
org_h, org_w = target_image.size
patch_h, patch_w = source_image.size

paste_left, paste_top = random.randint(0, org_w - patch_w), random.randint(0, org_h - patch_h)


target_image.paste(source_image, (paste_left, paste_top))

# 显示或保存结果图像
target_image.show()
target_image.save('result.jpg')