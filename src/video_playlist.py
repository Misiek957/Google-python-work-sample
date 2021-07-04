"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name):
        self.name = playlist_name
        self.videos = []  # list of video_ids

    def add_video(self, video_id):
        self.videos.append(video_id)

    # return True on success, False otherwise
    def remove_video(self, video_id):
        try:
            self.videos.remove(video_id)
            return True
        except ValueError:
            print("Cannot remove video from "+self.name+": Video is not in playlist")
            return False

    def get_name(self):
        return self.name

    def get_videos(self):
        return self.videos


