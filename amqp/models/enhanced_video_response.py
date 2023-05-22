import json
from .video_enhance_request import VideoEnhanceRequest

class EnhancedVideoResponse:
    def __init__(self, video_enhance_request: VideoEnhanceRequest, enhancedVideoUrl: str, status: str, statusMessage: str):
        self.userId = video_enhance_request.userId
        self.requestId = video_enhance_request.requestId
        self.videoUrl = video_enhance_request.videoUrl
        self.enhancedVideoUrl = enhancedVideoUrl
        self.status = status
        self.statusMessage = statusMessage
    
    def __str__(self):
        return f"VideoEnhanceRequest(userId={self.userId}, requestId={self.requestId}, videoUrl={self.videoUrl}), enhancedVideoUrl={self.enhancedVideoUrl}"
    
    def dumps(self):
        d = {
            "userId": self.userId,
            "requestId": self.requestId,
            "videoUrl": self.videoUrl,
            "enhancedVideoUrl": self.enhancedVideoUrl
        }
        return json.dumps(d)