import cv2
import imutils
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# ---- --------------- Xy ly ----------------------
def Xuly(img):
    #Chuyển ảnh sang đen trắng 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Làm mờ và mịn ảnh
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    # Xác định cạnh Canny
    edged = cv2.Canny(gray, 30, 200) 
    # tìm và tập hơp các điểm có giá trị màu tương tự (đen)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # sắp xếp các đường viền theo kích thước của chúng
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in contours:
        # Tìm chu vi đường viền khép kín của biển số xe
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    
        # xác định 4 góc của biển số xe
        # gán vào biến đường viền để xác định tiếp
        if len(approx) == 4:
            screenCnt = approx
            break

    # Kiểm tra xem đường viền vừa tìm có tồn tại không
    if screenCnt is None:
        detected = 0
        print ("No contour detected")
    else:
        detected = 1 

    # Xử lý và nhận dạng biển số vừa tìm được

    # Vẽ khung hình chữ nhật quanh biển số để đánh dấu
    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
    # Tạo mảng 2 chiều với các phần tử 0, với kích thước theo ảnh ban đầu
    mask = np.zeros(gray.shape,np.uint8)
    # Vẽ khung hình chữ nhật quanh vùng ảnh mới tạo
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    # Lấy vùng biển số từ ảnh ban đầu
    new_image = cv2.bitwise_and(img,img,mask=mask)

    # Xác đinh tọa độ hình chữ nhật biển số xe
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    return Cropped

# ------------------- end Xy ly --------------------------------

# ----------Xuat -------------------

# Sau khi đã xác định được vùng biển số
# Ta nhận dạng ký tự cua biển só bằng pytesseract
def Xuat(Cropped):
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    return text

# Ảnh biển số đã được cắt ra
def image_crop(Cropped): 
    x =  cv2.resize(Cropped,(300,100))
    cv2.imshow('Cropped',x)
    return

# --------- ham  danh dau image--------------
def DanhDau(img):
    #Chuyển ảnh sang đen trắng 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # Làm mờ và mịn ảnh
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    # Xác định cạnh Canny
    edged = cv2.Canny(gray, 30, 200) 
    # tìm và tập hơp các điểm có giá trị màu tương tự (đen)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # sắp xếp các đường viền theo kích thước của chúng
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in contours:
        # Tìm chu vi đường viền khép kín của biển số xe
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    
        # xác định 4 góc của biển số xe
        # gán vào biến đường viền để xác định tiếp
        if len(approx) == 4:
            screenCnt = approx
            break

    # Kiểm tra xem đường viền vừa tìm có tồn tại không
    if screenCnt is None:
        detected = 0
        print ("No contour detected")
    else:
        detected = 1 

    # Xử lý và nhận dạng biển số vừa tìm được

    # Vẽ khung hình chữ nhật quanh biển số để đánh dấu
    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
    # Tạo mảng 2 chiều với các phần tử 0, với kích thước theo ảnh ban đầu
    mask = np.zeros(gray.shape,np.uint8)
    # Vẽ khung hình chữ nhật quanh vùng ảnh mới tạo
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    # Lấy vùng biển số từ ảnh ban đầu
    new_image = cv2.bitwise_and(img,img,mask=mask)

    # Xác đinh tọa độ hình chữ nhật biển số xe
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    return img

# Ảnh biển số đã được danh dau
def image_sign(img): 
    x =  cv2.resize(img,(400,300))
    cv2.imshow('Sign',x)
    return
 

# Các lệnh chờ và xóa màn hình
cv2.waitKey(0)
cv2.destroyAllWindows()