import pprint
from types import SimpleNamespace

def p(x):
    pprint.pprint(x)

def get_dv(app, action, content):
    resolve = app.GetResolve()
    fusion = resolve.Fusion()
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    mediaPool = project.GetMediaPool()
    rootFolder = mediaPool.GetRootFolder()
    timeline = project.GetCurrentTimeline()
    mediaStorage = resolve.GetMediaStorage()
    
    # use dot notation to access properties
    return SimpleNamespace(**{
        "resolve": resolve,
        "fusion": fusion,
        "projectManager": projectManager,
        "project": project,
        "mediaPool": mediaPool,
        "mediaStorage": mediaStorage,
        "rootFolder": rootFolder,
        "timeline": timeline,

        "action": action,
        "content": content
    })

def find_track(dv, track_name, track_type):
    timeline = dv.timeline
    for i in range(timeline.GetTrackCount(track_type)):
        # Track の index は 1-based
        if timeline.GetTrackName(track_type, i+1) == track_name:
            return i + 1
    return None

def find_clip(root, clip_name):
    # print (root, clip_name)
    for clip in root.GetClipList():
        properties = clip.GetClipProperty() 
        if clip_name in properties['File Name'] or clip_name in properties['Clip Name']:
            return clip

    sub_folders = root.GetSubFolders()
    for index in sub_folders:
        clip = find_clip(sub_folders[index], clip_name)
        if clip != None:
            return clip
    
    return None

def find_first_empty_track_at_frame(dv, track_type, frame):
    timeline = dv.timeline
    track_count = timeline.GetTrackCount(track_type)

    for i in range(track_count):
        hasItemAtFrame = False
        items = timeline.GetItemListInTrack(track_type, i + 1)
        for item in items:
            if frame >= item.GetStart() and frame <= item.GetEnd():
                hasItemAtFrame = True
                break

        if hasItemAtFrame == False: 
            return i + 1

    return track_count + 1
            

# まじで感謝-b0sh
# https://github.com/tomoki/DaVinciResolveVoiceroidScript/blob/master/main.py
def frameToTimecode(frame):
    # TODO: 01:00:00 以外からもスタートできるようにする。
    frameRate = dv.project.GetSetting("timelineFrameRate")
    # 秒の計算で余りが出ると面倒なので先にフレームの部分だけ計算しておく。
    remainder = frame % frameRate
    frame -= remainder
    second = frame / frameRate
    hour = second // (60 * 60)
    second -= hour * (60 * 60)
    minute = second // 60
    second -= minute * 60

    return f"%02d:%02d:%02d:%02d"%(hour, minute, second, remainder)


def timecode2Frame(tc: str, fps):
    int_fps = {
        23: 24,
        29: 30,
        47: 48,
        59: 60,
        95: 96,
        119: 120,
    }
    if fps in int_fps.keys():
        fps = int_fps[fps]
    is_DF = False
    if ';' in tc:
        is_DF = True
        tc = tc.replace(';', ':')
    t = tc.split(':')
    h = int(t[0])
    m = int(t[1]) + (h * 60)
    s = int(t[2]) + (m * 60)
    f = int(t[3]) + (s * fps)
    drop_frames = 0
    if is_DF:
        _f = fps / 15
        drop_frames = _f * (m - (m // 10))
    return f - drop_frames

def get_current_frame(timeline):
    timecode = timeline.GetCurrentTimecode()
    fps = int(timeline.GetSetting('timelineFrameRate'))
    return timecode2Frame(timecode, fps)

