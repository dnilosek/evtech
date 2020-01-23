import argparse
import evtech
import cv2

# Load arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d",
                    "--dataset",
                    help="Location of dataset",
                    type=str)
args = parser.parse_args()

# Only care about obliques for this app
_, obliques = evtech.load_dataset(args.dataset)

# Load first oblique image
img = obliques[0].load_image()

# mouse callback function
# For drawing
drawing = False # true if mouse is pressed
ix,iy = -1,-1
def draw_line(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing:
            drawing = False
            # Draw line
            cv2.line(img,pt1=(ix,iy),pt2=(x,y),color=(0,0,255),thickness=3)

            # Compute height
            height = obliques[0].height_between_points([ix,iy],[x,y])

            # Computed in meters, convert to feet
            height *= 3.28084
            
            # Label line
            lbl = "{:.2f}".format(height) + " feet"
            cv2.putText(img, lbl, (x+10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        else:
            drawing = True
            ix,iy = x,y

# Making Window For The Image
cv2.namedWindow("Image")
# Adding Mouse CallBack Event
cv2.setMouseCallback("Image",draw_line)

# Starting The Loop So Image Can Be Shown
while(True):
    cv2.imshow("Image",img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()