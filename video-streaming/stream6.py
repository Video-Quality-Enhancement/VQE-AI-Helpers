import ffmpeg

# Create a video stream from the audio file.
audio_stream = ffmpeg.input('audio.mp3')

# Create a buffer to store the frames.
frames = []

# Start streaming the audio.
server = ffmpeg.run_server(audio_stream, port=8080)

i = 0
# Start receiving frames.
while True:
    # Get the next frame.
    frame = ffmpeg.input(f'frame_{i}.jpg')

    # Add the frame to the buffer.
    frames.append(frame)

    # If the buffer is full, send the frames to the HTTP server.
    if len(frames) == 10:
        combined_stream = ffmpeg.join(frames)
        server.send_stream(combined_stream)
        frames = []

    i += 1
    
    # Wait for the user to stop streaming.
    input('Press enter to stop streaming.')

# Stop streaming the audio.
server.stop()
