import ffmpeg

video_format = "flv"
server_url = "http://127.0.0.1:8080"

def main():
    input_video = ffmpeg.input("video_preview_h264.mp4")
    merged_audio = ffmpeg.input("1-minute-rain-medium-6767.mp3")
    (
        ffmpeg
        .concat(input_video, merged_audio, v=1, a=1)
        .output(
            server_url, 
            listen=1, # enables HTTP server
            f=video_format)
        .global_args("-re") # argument to act as a live stream
        .run(cmd=r'D:\Program Files\ffmpeg\bin\ffmpeg.exe')
    )

main()