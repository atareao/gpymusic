import abc
import subprocess
import api_user


class MusicObject(abc.ABC):
    def __init__(self, name, id):
        self.name = name
        self.id = id

    @abc.abstractmethod
    def to_string(self):
        # returns formatted info on the MusicObject
        return

    @abc.abstractmethod
    def play(self):
        # streams the MusicObject
        return

    @abc.abstractmethod
    def show(self):
        # prints a the MusicObject's formatted info
        return


# ------------------------------------------------------------

class Artist(MusicObject):
    def __init__(self, artist):
        self.contents = {}
        if 'albums' in artist:
            self.contents['albums'] = [{'name': album['name'], 'id': album['albumId']} for album in artist['albums']]
        else:
            self.contents['albums'] = {}
        if 'topTracks' in artist:
            self.contents['songs'] = [{'name': song['title'], 'id': song['storeId']} for song in artist['topTracks']]
        else:
            self.contents['songs'] = {}
        super().__init__(artist['name'], artist['artistId'])

    def length(self):
        return sum([len(self.contents[key]) for key in self.contents])

    def to_string(self):
        return self.name

    def play(self):
        for song in self.contents['songs']:
            url = api_user.API.get_stream_url(song['id'])
            print('Playing %s:' % (' - '.join((self.name, song['name']))))
            if subprocess.call(['mpv', '--really-quiet', '--input-conf=~/.config/pmcli/mpv_input.conf', url]) is 11:
                break

    def show(self):
        i = 1
        print('%d: %s' % (i, self.to_string()))
        i += 1
        print('Albums:')
        for album in self.contents['albums']:
            print('%d: %s' % (i, album['name']))
            i += 1
        print('Songs:')
        for song in self.contents['songs']:
            print('%d: %s' % (i, song['name']))
            i += 1


# ------------------------------------------------------------

class Album(MusicObject):
    def __init__(self, album):
        self.contents = {}
        self.contents = {'artist': {'name': album['artist'], 'id': album['artistId']},
                         'songs': [{'name': song['title'], 'id': song['storeId']} for song in album['tracks']]}
        super().__init__(album['name'], album['albumId'])

    def length(self):
        return len(self.contents['songs'])

    def to_string(self):
        return ' - '.join((self.contents['artist']['name'], self.name))

    def play(self):
        for song in self.contents['songs']:
            url = api_user.API.get_stream_url(song['id'])
            print('Playing %s:' % (' - '.join((self.contents['artist']['name'], song['name'], self.name))))
            if subprocess.call(['mpv', '--really-quiet', '--input-conf=~/.config/pmcli/mpv_input.conf', url]) is 11:
                break

    def show(self):
        i = 1
        print('%d: %s' % (i, self.to_string()))
        i += 1
        print('Songs:')
        for song in self.contents['songs']:
            print('%d: %s' % (i, song['name']))
            i += 1


# ------------------------------------------------------------

class Song(MusicObject):
    def __init__(self, song):
        self.contents = {'artist': {'name': song['artist'], 'id': song['artistId'][0]},
                         'album': {'name': song['album'], 'id': song['albumId']}}
        super().__init__(song['title'], song['storeId'])

    def length(self):
        return 1

    def to_string(self):
        return ' - '.join((self.contents['artist']['name'], self.name, self.contents['album']['name']))

    def play(self):
        url = api_user.API.get_stream_url(self.id)
        print('Playing %s:' % self.to_string())
        subprocess.call(['mpv', '--really-quiet', url])

    def show(self):
        print('1: %s' % (self.to_string()))
