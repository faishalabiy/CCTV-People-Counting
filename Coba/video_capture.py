import cv2
from datetime import datetime

cap = cv2.VideoCapture(0);

print(cap.isOpened())

#trigger capture
isTriggered = False
#if LRTMainCpuMvb send signal, isTriggered = True

#akan melakukan capture sekali hitungan setelah berjalan dan selanjutnya setelah break
while(cap.isOpened()):

    time = datetime.now()
    timeName = datetime.isoformat(time)
    print(timeName)

    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.imwrite('capture_.'+timeName+'jpg', frame)

    #print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()

