import cv2    # computer vision module
import cvzone # hand tracking module
from cvzone.HandTrackingModule import HandDetector # hand detector class
import time as t  # time module
import random # random module

cam = cv2.VideoCapture(0) 
cam.set(3, 400) # width
cam.set(4, 420) # height

detector = HandDetector(maxHands=1) # hand detector object
timer = 0 
result_user = False 
start_game = False
scores = [0, 0] # [AI, player]

while True:
    game_bg_img = cv2.imread("images/game_bg_img.png")
    success, cam_img = cam.read()
    scaled_cam_img = cv2.resize(cam_img, (0, 0), None, 0.875, 0.875) # height scaled
    scaled_cam_img = scaled_cam_img[:, 80:480]                       # width scaled
    
    # find hand landmarks
    hand_landmarks, cam_img = detector.findHands(scaled_cam_img, draw=False)
    
    if start_game: # if start game is true (game has started) when pressed 's' key  
        if result_user == False: 
            timer = t.time() - initial_time # time elapsed since game started
            cv2.putText(game_bg_img, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 5) # timer text
            if timer>3:
                result_user = True
                timer = 0
                if hand_landmarks: # if hand landmarks are detected
                    hand_landmark = hand_landmarks[0] # first hand
                    fingers = detector.fingersUp(hand_landmark) # how many fingers are up for this hand
                    # print(fingers)    
                    if fingers == [0, 0, 0, 0, 0]: # rock
                        player_move = 1
                    if fingers == [1, 1, 1, 1, 1]: # paper
                        player_move = 2
                    if fingers == [0, 1, 1, 0, 0]: # scissors
                        player_move = 3
                    else: 
                        print("No hand detected")    
                    
                    random_move = random.randint(1, 3) # random move for AI    
                    ai_img = cv2.imread(f'images/{random_move}.png', cv2.IMREAD_UNCHANGED)
                    game_bg_img = cvzone.overlayPNG(game_bg_img, ai_img, (149, 310))  # overlay image(rock) on game background image
                    
                    # player wins
                    if (player_move == 1 and random_move == 3) or \
                       (player_move == 2 and random_move == 1) or \
                       (player_move == 3 and random_move == 2):
                        scores[1] += 1
                        
                    # ai wins
                    if (player_move == 3 and random_move == 1) or \
                       (player_move == 1 and random_move == 2) or \
                       (player_move == 2 and random_move == 3):
                        scores[0] += 1
                        
                    #print(player_move)

    # overlay scaled camera image on game background image
    game_bg_img[234:654, 795:1195] = scaled_cam_img # (y1:y2, x1:x2), (height, width)
    
    if result_user:
        game_bg_img = cvzone.overlayPNG(game_bg_img, ai_img, (149, 310)) 
    
    cv2.putText(game_bg_img, str((scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6) 
    cv2.putText(game_bg_img, str((scores[1])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6) 
    
    #cv2.imshow("Camera", cam_img)
    cv2.imshow("Game Background Image", game_bg_img)
    #cv2.imshow("Scaled Camera", scaled_cam_img)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        start_game = True
        initial_time = t.time() # initial time when game starts
        result_user = False
