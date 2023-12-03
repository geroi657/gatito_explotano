import os

path = 'assets/cat_2/'

images = os.listdir(path)

# while len(images) > 30:
#     for i in range(len(images)):
#         os.rename(path + images[i], f'{path}{i + 1}.png')
#     images = os.listdir(path)
#     for i in range(1, len(images), 2):
#         os.remove(path+images[i])
#     images = os.listdir(path)

for i in range(len(images)):
    os.rename(path + images[i], f'{path}{i + 1}.png')