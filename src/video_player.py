"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
import sys, os


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video_id = None  # the video_id of the playing Video object, is a string
        self._video_paused = False  # Boolean status variable indicating whether current video is paused
        self._playlists = []  # is a List<Playlist>
        self._number_of_allowed_videos = len(self._video_library.get_all_videos())

    # return video_title given video_id, none if invalid id
    def get_title(self, video_id):
        currentVideoInfo = self._video_library.get_video(video_id)
        if currentVideoInfo is None:
            return None
        else:
            return currentVideoInfo.title

    def get_video(self, video_id):
        return self._video_library.get_video(video_id)

    def get_tags(self, video_id):  # return tags(list of string) given id
        currentVideoInfo = self._video_library.get_video(video_id)
        return currentVideoInfo.tags

    # get the index of given name in self._playlists
    def get_playlist_index(self, playlist_name):
        for playlist in self._playlists:
            if playlist_name.upper() == playlist.get_name().upper():
                return self._playlists.index(playlist)
        return None

    # returns a playlist object
    def get_playlist(self, playlist_name):
        index = self.get_playlist_index(playlist_name)
        return self._playlists[index]

    # return a string representation of a video
    def get_video_info_string(self, video_id):
        video = self._video_library.get_video(video_id)
        tag_string = ""
        for tag in video.tags:
            tag_string += tag + " "
        tag_string = tag_string.strip()
        result = video.title + " (" + video.video_id + ") [" + tag_string + "]"
        if video.flagged:
            result = result + " - FLAGGED " + "(reason: " + video.flag_reason + ")"
        return result

    # returns printable format of flag reason, (reason: Not supplied) for empty reason
    def get_flag_reason(self, video_id) -> str:
        video = self._video_library.get_video(video_id)
        if video.flag_reason == "":
            return "(reason: Not supplied)"
        else:
            return "(reason: " + video.flag_reason + ")"

    @staticmethod
    def block_print():
        sys.stdout = open(os.devnull, 'w')

    @staticmethod
    def enable_print():
        sys.stdout = sys.__stdout__

    def number_of_allowed_videos(self) -> int:
        return self._number_of_allowed_videos

    def increment_number_of_allowed_videos(self):
        self._number_of_allowed_videos += 1

    def decrement_number_of_allowed_videos(self):
        self._number_of_allowed_videos -= 1

    # ------------------------ ↑ customised functions ↑ -----------------------------

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videoList = []
        print("Here's a list of all available videos:")
        all_videos = self._video_library.get_all_videos()
        for video in all_videos:
            video_string = self.get_video_info_string(video.video_id)
            videoList.append(video_string)
        videoList = sorted(videoList)
        for videoInfo in videoList:
            print(videoInfo)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        currentVideoInfo = self._video_library.get_video(video_id)
        if currentVideoInfo is None:  # if input is an invalid id
            print("Cannot play video: Video does not exist")
        else:  # if a valid video_id is input
            if currentVideoInfo.flagged:
                reason = self.get_flag_reason(video_id)
                print("Cannot play video: Video is currently flagged "+reason)
                return
            if self._video_paused:
                self.stop_video()
                self._video_paused = False
            if self._current_video_id is not None:
                self.stop_video()
            self._current_video_id = video_id
            currentVideoTitle = currentVideoInfo.title
            print("Playing video: " + currentVideoTitle)

    def stop_video(self):
        """Stops the current video."""
        if self._current_video_id is None:
            print("Cannot stop video: No video is currently playing")
        else:
            currentVideoTitle = self.get_title(self._current_video_id)
            print("Stopping video: " + currentVideoTitle)
            self._current_video_id = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        VideoList = self._video_library.get_all_videos()
        VideoIDList = []
        for elem in VideoList:
            VideoIDList.append(elem.video_id)
        randomVideoID = random.choice(VideoIDList)
        if self.number_of_allowed_videos() == 0:
            print("No videos available")
            return
        else:
            self.play_video(randomVideoID)

    def pause_video(self):
        """Pauses the current video."""

        if self._video_paused:
            title = self.get_title(self._current_video_id)
            print("Video already paused: " + title)
        elif self._current_video_id is None:
            print("Cannot pause video: No video is currently playing")
        else:
            self._video_paused = True
            title = self.get_title(self._current_video_id)
            print("Pausing video: " + title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self._current_video_id is None:
            print("Cannot continue video: No video is currently playing")
        elif not self._video_paused:
            print("Cannot continue video: Video is not paused")
        else:
            self._video_paused = False
            print("Continuing video: " + self.get_title(self._current_video_id))

    def show_playing(self):
        """Displays video currently playing."""
        title = self.get_title(self._current_video_id)
        if title is None:
            print("No video is currently playing")
        else:
            id = self._current_video_id
            tagS = ""
            for tag in self.get_tags(id):
                tagS += tag + " "
            tagS = tagS.strip()
            # elemVideo = elem.title + " (" + elem.video_id + ") [" + tagS + "]"
            message = "Currently playing: " + title + " (" + id + ") [" + tagS + "]"
            if self._video_paused:
                message += " - PAUSED"
            print(message)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        NAME = playlist_name.upper()  # capitalised name for uniformity
        # comparison of newPlaylist with all existing playlists
        for elem in self._playlists:
            if elem.name.upper() == NAME:
                print("Cannot create playlist: A playlist with the same name already exists")
                return None
        newPlaylist = Playlist(playlist_name)
        print("Successfully created new playlist: " + playlist_name)
        self._playlists.append(newPlaylist)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlistIndex = self.get_playlist_index(playlist_name)
        if playlistIndex is None:
            # Playlist with the input name is not found
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        elif self.get_title(video_id) is None:
            print("Cannot add video to " + playlist_name + ": Video does not exist")
        elif self.get_video(video_id).flagged:
            print("Cannot add video to " + playlist_name + ": Video is currently flagged " + self.get_flag_reason(video_id))
            return
        else:
            playlist = self._playlists[playlistIndex]
            if video_id in playlist.get_videos():
                print("Cannot add video to " + playlist_name + ": Video already added")
            else:
                playlist.add_video(video_id)
                print("Added video to " + playlist_name + ": " + self.get_title(video_id))

    def show_all_playlists(self):
        """Display all playlists."""
        playlistDisplay = []
        for playlist in self._playlists:
            playlistDisplay.append(playlist.get_name())
        if not playlistDisplay:
            # if no playlists, no playlist to show - test_show_all_playlists_no_playlists_exist
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for elem in sorted(playlistDisplay):
                print(elem)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_index = self.get_playlist_index(playlist_name)
        if playlist_index is None:  # Playlist with the input name is not found
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Showing playlist: " + playlist_name)
            playlist = self._playlists[playlist_index]
            video_ids = playlist.get_videos()
            if len(video_ids) == 0:  # no videos in videos[]
                print("No videos here yet")
            else:
                for video_id in video_ids:
                    print(self.get_video_info_string(video_id))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_index = self.get_playlist_index(playlist_name)
        if playlist_index is None:
            # Playlist with the input name is not found
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
        else:
            playlist = self.get_playlist(playlist_name)
            if self.get_title(video_id) is None:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
            elif playlist.remove_video(video_id):
                print("Removed video from " + playlist_name + ": " + self.get_title(video_id))

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_index = self.get_playlist_index(playlist_name)
        if playlist_index is None:
            # Playlist with the input name is not found
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
            return
        playlist = self.get_playlist(playlist_name)
        self.block_print()
        for video_id in playlist.videos:
            self.remove_from_playlist(playlist_name, video_id)
        self.enable_print()
        print('Successfully removed all videos from ' + playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_index = self.get_playlist_index(playlist_name)
        if playlist_index is None:
            print('Cannot delete playlist ' + playlist_name + ': Playlist does not exist')
        else:
            self._playlists.pop(playlist_index)
            print('Deleted playlist: ' + playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        matching_video_ids = []
        # populate matching_video_ids
        for video in all_videos:
            if video.flagged:
                continue
            index = video.title.upper().find(search_term.upper())
            # index = -1 if value not found
            if index != -1:
                matching_video_ids.append(video.video_id)
        if len(matching_video_ids) == 0:
            print('No search results for ' + search_term)
            return
        else:
            print('Here are the results for ' + search_term + ':')
            for i in range(len(matching_video_ids)):
                print(str(i + 1) + ") " + self.get_video_info_string(matching_video_ids[i]))
            try:
                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")
                response = input()
                if int(response) <= len(matching_video_ids):
                    video_id_to_play = matching_video_ids[int(response) - 1]
                    self.play_video(video_id_to_play)
            except ValueError:
                return

            # for i, video_id in enumerate(matching_video_ids):
            #     print(str(i)+") " + self.get_video_info_string(video_id))

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        matching_video_ids = []
        # populate matching_video_ids
        for video in all_videos:
            if video.flagged:
                continue
            if video_tag in video.tags:
                matching_video_ids.append(video.video_id)
        if len(matching_video_ids) == 0:
            print('No search results for ' + video_tag)
            return
        else:
            print('Here are the results for ' + video_tag + ':')
            for i in range(len(matching_video_ids)):
                print(str(i + 1) + ") " + self.get_video_info_string(matching_video_ids[i]))
            try:
                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")
                response = input()
                if int(response) <= len(matching_video_ids):
                    video_id_to_play = matching_video_ids[int(response) - 1]
                    self.play_video(video_id_to_play)
            except ValueError:
                return

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        flag_success = self._video_library.flag_video(video_id, flag_reason)
        if flag_success:
            if self._current_video_id == video_id:
                self.stop_video()
            print("Successfully flagged video: " + self.get_title(video_id) + " " + self.get_flag_reason(video_id))
            self.decrement_number_of_allowed_videos()
        else:
            return

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        allow_success = self._video_library.allow_video(video_id)
        if allow_success:
            print('Successfully removed flag from video: ' + self.get_title(video_id))
            self.increment_number_of_allowed_videos()
        else:
            return
