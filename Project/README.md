# Title: Home Security - Alert System

This project is to alert home owners/registered users when an unknown person enters into the home territory. It is implemented using computer vision and deep learning technologies on a RPi3 board with a camera module.

## Approach:
The system reads camera feed continously and analyzes every alternate frame. If any faces are detected in the frame, then it compares them against the registered user data (stored in MongoDB). If the faces are new, then it uploads the image to GCS. The GCS has a put trigger that invokes a cloud function that sends an automatic message to a Discord channel.

## System Overview:
![system_overview](https://user-images.githubusercontent.com/32699857/205792933-b3c336a0-dbe0-4992-aea1-3907b9b460a2.png)

## Result
![Discord Messages](https://user-images.githubusercontent.com/32699857/205789421-78d820ae-6ea0-4b22-8640-603d39084b4c.png)
