import os
import uuid
from lib import *

def action_get_frame(dv):

    current_page = dv.resolve.GetCurrentPage()
    prefix = "davinci-resolve-export"
    extension = "png" # Can also use jpg
    project_folder = '''C:\YouTube'''
    with open('C:\\YouTube\\Scripts\\activeproject.txt') as f:
        project_folder = f.readlines()[0]
    
    print(project_folder)

    # -------------------------------------------------------------
    # Actual Davinci API Calls to create color page stills
    frames = [ dv.timeline.GrabStill() ]
    dv.stillAlbum.ExportStills(frames, project_folder, prefix, extension)
    dv.stillAlbum.DeleteStills(frames)
    # -------------------------------------------------------------

    if (current_page != 'color'):
        dv.resolve.OpenPage(current_page)


    directory = project_folder + "//"
    for filename in os.listdir(directory):
        if prefix in filename:
            file, ext = os.path.splitext(filename)
            
            if ext == ".drx":
                try:
                    # rename the .png file
                    os.rename(
                        directory + file + "." + extension,
                        directory + "export-" + str(uuid.uuid4())[:8] + "." + extension
                    )
                    print(f'Renamed {file + ".png"} to {file + "_renamed.png"}')

                    os.remove(directory + filename)
                    print(f'Deleted {filename}')

                except FileNotFoundError:
                    print(f'Skipped {filename} due to missing corresponding .png file')
