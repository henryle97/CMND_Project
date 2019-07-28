import  matplotlib.pyplot as plt 
from PIL import Image
padding = 50
img = Image.open('./result/res_30x.jpg')
w,h = img.size
print(w)

w_new = w + padding * 2
h_new = h + padding * 2

new_img = Image.new('RGB',(w_new,h_new), (255,255,255))
new_img.paste(img, (padding,padding))
new_img.save('')
plt.imshow(new_img)
plt.show()