import json

class VideoEnhanceRequest:
    def __init__(self, userId, requestId, videoUrl):
        self.userId = userId
        self.requestId = requestId
        self.videoUrl = videoUrl
    
    def __str__(self):
        return f"VideoEnhanceRequest(userId={self.userId}, requestId={self.requestId}, videoUrl={self.videoUrl})"
    
    def loads(cls, bytes):
        d = json.loads(bytes)
        return cls(**d)