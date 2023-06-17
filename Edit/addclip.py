from lib import *
import os

def action_add_sfx(dv):
    clip = find_clip(dv.rootFolder, dv.content)
    sfx_track_id = find_track(dv, "SFX", "audio")

    if clip != None and sfx_track_id != None:
        print(f"Adding SFX clip {clip.GetClipProperty()['File Name']} at track #{sfx_track_id}")

        insertClipAtPlayhead(dv, sfx_track_id, clip)
    else:
        print ("Not found")

def action_add_clip(dv):
    clip = find_clip(dv.rootFolder, dv.content)

    frame = get_current_frame(dv.timeline)
    track_id = find_first_empty_track_at_frame(dv, "video", frame)

    print("Current frame:", frame)

    if clip != None and track_id != None:
        # print(clip, track_id, clip.GetClipProperty()['File Name'])

        insertClipAtPlayhead(dv, track_id, clip)
    else:
        print ("Not found")

def action_add_new_clip(dv):
    path = dv.content
    if os.path.isfile(path):
        dv.mediaStorage.AddItemListToMediaPool(path)

        dv.content = os.path.basename(path)

        action_add_clip(dv)
    else:
        print (path, "file not found")


def insertClipAtPlayhead(dv, track, clip):
    timeline = dv.timeline
    frame = get_current_frame(timeline)
    print("Current frame:", frame)

    subClip = {
        "mediaPoolItem": clip,
        "startFrame": 0,
        "endFrame":  60,
        "recordFrame": frame,
        "trackIndex": track,
    }

    # Returns a list of timeline items
    results = dv.mediaPool.AppendToTimeline([ subClip ]) 

    if len(results) > 0 and results[0] != None:
        return True

    print("Failed to add clip to timeline")
    return False

    