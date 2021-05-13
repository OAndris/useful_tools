from moviepy.editor import *

start = 37*60
end = 41*60 + 12.5
video = VideoFileClip("videoplayback.mp4").subclip(start, end)

result = CompositeVideoClip([video])
result.write_videofile("out.mp4")
