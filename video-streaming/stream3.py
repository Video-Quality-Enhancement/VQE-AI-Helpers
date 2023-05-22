import ffmpeg

def main():
    input_video = ffmpeg.input("video_preview_h264.mp4")
    merged_audio = ffmpeg.input("1-minute-rain-medium-6767.mp3")
    (
        ffmpeg
        .concat(input_video, merged_audio, v=1, a=1)
        .output("mix_delayed_audio.mp4")
        .run(overwrite_output=True, cmd=r'D:\Program Files\ffmpeg\bin\ffmpeg.exe')
    )

main()