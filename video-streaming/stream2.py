import ffmpeg
import cv2

def create_video_chunk(frame, audio_file):
  """Creates a video chunk from a frame and an audio file.

  Args:
    frame: The frame to create the video chunk from.
    audio_file: The audio file to add to the video chunk.

  Returns:
    A video chunk.
  """

  # Encode the frame.
  encoded_frame = ffmpeg.encode(frame)

  # Create a video stream.
  video_stream = ffmpeg.input(encoded_frame)

  # Add the audio stream.
  video_stream = ffmpeg.concat([video_stream, audio_file], stream_mapping={'0': '0', '1': '1'})

  # Create a video chunk.
  video_chunk = ffmpeg.output(video_stream, filename='/content/drive/MyDrive/video stream trail/output.mp4')

  # Return the video chunk.
  return video_chunk

"""4. Create a function to stream a video chunk:"""

def stream_video_chunk(video_chunk):
  """Streams a video chunk.

  Args:
    video_chunk: The video chunk to stream.

  """

  # Create a web server.
  server = ffmpeg.run_server(video_chunk, '0.0.0.0', 8080)

  # Serve the video chunk.
  server.serve_forever()

"""5. Create a function to create and stream video chunks from frames and one audio file:"""

def create_and_stream_video_chunks(frames, audio_file):
  """Creates and streams video chunks from frames and one audio file.

  Args:
    frames: The frames to create the video chunks from.
    audio_file: The audio file to add to the video chunks.

  """

  # Create a video chunk from each frame.
  for frame in frames:
    video_chunk = create_video_chunk(frame, audio_file)

    # Stream the video chunk.
    stream_video_chunk(video_chunk)

"""6. Call the function to create and stream video chunks from frames and one audio file:"""

def split_video_into_chunks(video_path, chunk_duration):
    video = cv2.VideoCapture(video_path)
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    chunk_frames = int(chunk_duration * frame_rate)
    num_chunks = int(total_frames / chunk_frames)
    
    chunks = []
    
    for i in range(num_chunks):
        frames = []
        for _ in range(chunk_frames):
            ret, frame = video.read()
            if not ret:
                break
            frames.append(frame)
        if frames:
            chunks.append(frames)
    
    video.release()
    return chunks, frame_rate

chunk_duration = 10  # Duration of each video chunk in seconds
chunks, frame_rate = split_video_into_chunks("video_preview_h264.mp4", chunk_duration)
audio_file = "1-minute-rain-medium-6767.mp3"

for chunk_frames in chunks:
    create_and_stream_video_chunks(chunk_frames, audio_file)

"""This code will create and stream video chunks from frames and one audio file. You can then access the video chunks by opening a web browser and navigating to `http://localhost:8080`."""