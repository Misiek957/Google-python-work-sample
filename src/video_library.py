"""A video library class."""

from .video import Video
from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}  # contains video objects
        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                    False,  # default flagged
                    ""  # default flag reason
                )

    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id) -> Video:
        """Returns the video object (title, url, tags, flagged_status, flagged message) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)

    # return True on success
    def flag_video(self, video_id, reason=""):
        video = self.get_video(video_id)
        if video:
            if video.flagged is True:
                print("Cannot flag video: Video is already flagged")
                return False
            else:  # if video is not flagged yet
                video._flagged = True
                video._flag_reason = reason
                return True
        else:  # if video nonexistent
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        video = self.get_video(video_id)
        if video:
            if video.flagged is False:
                print("Cannot remove flag from video: Video is not flagged")
                return False
            else:  # if video is already flagged
                video._flagged = False
                video._flag_reason = ""
                return True
        else:  # if video nonexistent
            print("Cannot remove flag from video: Video does not exist")

