import cv2
import moviepy.editor as mp

# Step 1: Splitting the Video into Chunks
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

# Step 2: Combining Frames with Audio
def combine_frames_with_audio(frames, audio_path, frame_rate):
    audio = mp.AudioFileClip(audio_path)
    frame_duration = 1.0 / frame_rate
    
    # Create an array of timestamps for each frame
    timestamps = [i * frame_duration for i in range(len(frames))]
    
    # Create a VideoClip from the frames with corresponding timestamps
    video = mp.VideoClip(lambda t: frames[int(t / frame_duration)], duration=len(frames) * frame_duration)
    
    # Set audio and timestamps
    video = video.set_audio(audio)
    video = video.set_duration(audio.duration)
    video = video.set_fps(frame_rate)
    
    final_video = video
    
    return final_video

# Step 3: Encoding and Streaming the Video Chunk
def stream_video_chunk(final_video):
    final_video.write_videofile('output_chunk.mp4', codec='libx264', audio_codec='aac', fps=final_video.fps)

# Example usage
video_path = "video_preview_h264.mp4" # 'input_video.mp4'
audio_path = "1-minute-rain-medium-6767.mp3" # 'input_audio.wav'
chunk_duration = 10  # Duration of each video chunk in seconds

chunks, frame_rate = split_video_into_chunks(video_path, chunk_duration)

for chunk_frames in chunks:
    final_video = combine_frames_with_audio(chunk_frames, audio_path, frame_rate)
    stream_video_chunk(final_video)