import time
from models import VideoEnhanceRequest
from models import EnhancedVideoResponse


def enhance_720p_video(video_enhance_request: VideoEnhanceRequest) -> EnhancedVideoResponse:
    print(video_enhance_request)
    
    # perform action here
    time.sleep(2)

    # set output variables
    enhanced_video_url = "https://download.samplelib.com/mp4/sample-5s.mp4"
    status = "success"
    statusMessage = "Video enhanced successfully"

    # create response object
    enhanced_video_response = EnhancedVideoResponse(video_enhance_request, enhanced_video_url, status, statusMessage)
    return enhanced_video_response