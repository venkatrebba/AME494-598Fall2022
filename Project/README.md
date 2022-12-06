Title: Home Security - Alert System

This project is to alert home owners/registered users when an unknown person enteres into the home terrioroty. It is implemented computer vision and deep learning technologies by utilizing RPi3 board with a camera module.

Approach:
The system reads camera feed continously and analyzes alternate frame. If any faces are detected in the frame, then it compares them against the registered user data (stored in MongoDB). If the faces are new, then it uploads the image to GCS. The GCS has a put trigger that invokes a cloud function to send a message to the Discord channel.

System Overview:
!(["System overview"] System Overview.png)


