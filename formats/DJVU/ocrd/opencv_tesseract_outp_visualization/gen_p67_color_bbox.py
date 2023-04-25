import cv2


img = cv2.imread('djvu2tess_p67.tiff')
height = img.shape[0]


with open('opencv_formatted_coords.txt', 'r') as input:
        for line in input.readlines():
            line = line.split(' ')[:-1]  # for excluding ''
            line = [int(a.strip(' ')) for a in line]
            x1y1 = (line[0], height - line[1])
            x2y2 = (line[2], height - line[3])
            cv2.rectangle(img, x1y1, x2y2, (line[4:]), 2)


cv2.imwrite('p67_bbox_color.png', img)
