# -*- coding: utf-8 -*-

'''
    GOtv XBMC Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
try:    import StorageServer
except: import storageserverdummy as StorageServer
from metahandler import metahandlers
from metahandler import metacontainers


action              = None
common              = CommonFunctions
metaget             = metahandlers.MetaData(preparezip=False)
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonDesc           = language(30450).encode("utf-8")
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonPoster         = os.path.join(addonPath,'resources/art/Poster.png')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
offData             = os.path.join(dataPath,'offset.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')
subData             = os.path.join(dataPath,'subscriptions.cfg')


class main:
    def __init__(self):
        global action
        index().container_data()
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        tvdb = urllib.unquote_plus(params["tvdb"])
        except:     tvdb = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        show_alt = urllib.unquote_plus(params["show_alt"])
        except:     show_alt = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb, year)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb, year)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'subscription_add':          contextMenu().subscription_add(name, url, image, imdb, year)
        elif action == 'subscription_from_search':  contextMenu().subscription_from_search(name, url, image, imdb, year)
        elif action == 'subscription_delete':       contextMenu().subscription_delete(name, url)
        elif action == 'subscriptions_update':      contextMenu().subscriptions_update()
        elif action == 'subscriptions_service':     contextMenu().subscriptions_update(silent=True)
        elif action == 'subscriptions_clean':       contextMenu().subscriptions_clean()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_seasons':              contextMenu().view('seasons')
        elif action == 'view_episodes':             contextMenu().view('episodes')
        elif action == 'metadata_tvshows':          contextMenu().metadata('tvshow', imdb, '', '')
        elif action == 'metadata_tvshows2':         contextMenu().metadata('tvshow', imdb, '', '')
        elif action == 'metadata_seasons':          contextMenu().metadata('season', imdb, season, '')
        elif action == 'metadata_episodes':         contextMenu().metadata('episode', imdb, season, episode)
        elif action == 'playcount_tvshows':         contextMenu().playcount('tvshow', imdb, '', '')
        elif action == 'playcount_seasons':         contextMenu().playcount('season', imdb, season, '')
        elif action == 'playcount_episodes':        contextMenu().playcount('episode', imdb, season, episode)
        elif action == 'library':                   contextMenu().library(name, url, imdb, year)
        elif action == 'download':                  contextMenu().download(name, title, imdb, tvdb, year, season, episode, show, show_alt)
        elif action == 'sources':                   contextMenu().sources(name, title, imdb, tvdb, year, season, episode, show, show_alt)
        elif action == 'autoplay':                  contextMenu().autoplay(name, title, imdb, tvdb, year, season, episode, show, show_alt)
        elif action == 'shows_favourites':          favourites().shows()
        elif action == 'shows_subscriptions':       subscriptions().shows()
        elif action == 'episodes_subscriptions':    subscriptions().episodes()
        elif action == 'shows':                     shows().imdb(url)
        elif action == 'shows_popular':             shows().imdb_popular()
        elif action == 'shows_rating':              shows().imdb_rating()
        elif action == 'shows_views':               shows().imdb_views()
        elif action == 'shows_active':              shows().imdb_active()
        elif action == 'shows_search':              shows().imdb_search(query)
        elif action == 'shows_trending':            shows().trakt_trending()
        elif action == 'genres_shows':              genres().imdb()
        elif action == 'seasons':                   seasons().get(url, image, year, imdb, genre, plot, show)
        elif action == 'episodes':                  episodes().get(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
        elif action == 'play':                      resolver().run(name, title, imdb, tvdb, year, season, episode, show, show_alt, url)

        if action is None:
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('seasons'):
            xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
            index().container_view('seasons', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class player(xbmc.Player):
    def __init__ (self):
        self.folderPath = xbmc.getInfoLabel('Container.FolderPath')
        self.loadingStarting = time.time()
        xbmc.Player.__init__(self)

    def run(self, name, url, imdb='0'):
        self.video_info(name, imdb)

        if self.folderPath.startswith(sys.argv[0]):
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try:
                file = self.name + '.strm'
                file = file.translate(None, '\/:*?"<>|')

                meta = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["title", "plot", "votes", "rating", "writer", "firstaired", "playcount", "runtime", "director", "productioncode", "season", "episode", "originaltitle", "showtitle", "lastplayed", "fanart", "thumbnail", "file", "resume", "tvshowid", "dateadded", "uniqueid"]}, "id": 1}' % (self.season, self.episode))
                meta = unicode(meta, 'utf-8', errors='ignore')
                meta = json.loads(meta)
                meta = meta['result']['episodes']
                self.meta = [i for i in meta if i['file'].endswith(file)][0]
                meta = {'title': self.meta['title'], 'tvshowtitle': self.meta['showtitle'], 'season': self.meta['season'], 'episode': self.meta['episode'], 'writer': str(self.meta['writer']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'director': str(self.meta['director']).replace("[u'", '').replace("']", '').replace("', u'", ' / '), 'rating': self.meta['rating'], 'duration': self.meta['runtime'], 'premiered': self.meta['firstaired'], 'plot': self.meta['plot']}
                poster = self.meta['thumbnail']
            except:
                meta = {'label': self.name, 'title': self.name}
                poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(1, 21):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def video_info(self, name, imdb):
        self.name = name
        self.content = 'episode'
        self.show = self.name.rsplit(' ', 1)[0]
        if imdb == '0': imdb = metaget.get_meta('tvshow', self.show)['imdb_id']
        self.imdb = re.sub('[^0-9]', '', imdb)
        self.season = '%01d' % int(name.rsplit(' ', 1)[-1].split('S')[-1].split('E')[0])
        self.episode = '%01d' % int(name.rsplit(' ', 1)[-1].split('E')[-1])
        self.subtitle = subtitles().get(self.name, self.imdb, self.season, self.episode)

    def offset_add(self):
        try:
            file = open(offData, 'a+')
            file.write('"%s"|"%s"|"%s"\n' % (self.name, self.imdb, self.currentTime))
            file.close()
        except:
            return

    def offset_delete(self):
        try:
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"|"%s"' % (self.name, self.imdb) in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(offData, 'w')
            for line in list: file.write(line)
            file.close()
        except:
            return

    def offset_read(self):
        try:
            self.offset = '0'
            file = xbmcvfs.File(offData)
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"|"%s"' % (self.name, self.imdb) in x][0]
            self.offset = re.compile('".+?"[|]".+?"[|]"(.+?)"').findall(line)[0]
        except:
            return

    def change_watched(self):
        try:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }' % str(self.meta['episodeid']))
        except:
            metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched=7)

    def container_refresh(self):
        try:
            params = {}
            query = self.folderPath[self.folderPath.find('?') + 1:].split('&')
            for i in query: params[i.split('=')[0]] = i.split('=')[1]
            if not params["action"].endswith('_search'): index().container_refresh()
        except:
            pass

    def resume_playback(self):
        offset = float(self.offset)
        if not offset > 0: return
        minutes, seconds = divmod(offset, 60)
        hours, minutes = divmod(minutes, 60)
        offset_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        yes = index().yesnoDialog('%s %s' % (language(30353).encode("utf-8"), offset_time), '', self.name, language(30354).encode("utf-8"), language(30355).encode("utf-8"))
        if yes: self.seekTime(offset)

    def onPlayBackStarted(self):
        try: self.setSubtitles(self.subtitle)
        except: pass

        if getSetting("playback_info") == 'true':
            elapsedTime = '%s %.2f seconds' % (language(30319).encode("utf-8"), (time.time() - self.loadingStarting))     
            index().infoDialog(elapsedTime, header=self.name)

        if getSetting("resume_playback") == 'true':
            self.offset_read()
            self.resume_playback()

    def onPlayBackEnded(self):
        self.change_watched()
        self.offset_delete()
        self.container_refresh()

    def onPlayBackStopped(self):
        if self.currentTime / self.totalTime >= .9:
            self.change_watched()
        self.offset_delete()
        self.offset_add()
        self.container_refresh()

class subtitles:
    def get(self, name, imdb, season, episode):
        if not getSetting("subtitles") == 'true': return
        quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']
        langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}

        langs = []
        try: langs.append(langDict[getSetting("sublang1")])
        except: pass
        try: langs.append(langDict[getSetting("sublang2")])
        except: pass
        langs = ','.join(langs)

        try:
            import xmlrpclib
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
            token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
            result = server.SearchSubtitles(token, [{'sublanguageid': langs, 'imdbid': imdb, 'season': season, 'episode': episode}])['data']
            result = [i for i in result if i['SubSumCD'] == '1']
        except:
            return

        subtitles = []
        for lang in langs.split(','):
            filter = [i for i in result if lang == i['SubLanguageID']]
            if filter == []: continue
            for q in quality: subtitles += [i for i in filter if q in i['MovieReleaseName'].lower()]
            subtitles += [i for i in filter if not any(x in i['MovieReleaseName'].lower() for x in quality)]
            try: lang = xbmc.convertLanguage(lang, xbmc.ISO_639_1)
            except: pass
            break

        try:
            import zlib, base64
            content = [subtitles[0]["IDSubtitleFile"],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = zlib.decompressobj(16+zlib.MAX_WBITS).decompress(content)

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            file = open(subtitle, 'wb')
            file.write(content)
            file.close()

            return subtitle
        except:
            index().infoDialog(language(30317).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

    def container_data(self):
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(subData):
            file = xbmcvfs.File(subData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
            file.write('')
            file.close()
        if not xbmcvfs.exists(offData):
            file = xbmcvfs.File(offData, 'w')
            file.write('')
            file.close()

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []
                if action.endswith('_subscriptions'):
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_update)' % (sys.argv[0])))
                    cm.append((language(30426).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_clean)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        if pageList == None: return

        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def showList(self, showList):
        if showList == None: return

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()
        file = xbmcvfs.File(subData)
        subRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, url, image, year, imdb, genre, plot = i['name'], i['url'], i['image'], i['year'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name

                sysname, sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot)
                u = '%s?action=seasons&url=%s&image=%s&year=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysyear, sysimdb, sysgenre, sysplot, sysname)

                if getSetting("meta") == 'true':
                    meta = metaget.get_meta('tvshow', title, imdb_id=imdb)
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub('[^0-9]', '', meta['imdb_id']))
                    poster, banner = meta['cover_url'], meta['banner_url']
                    if banner == '': banner = poster
                    if banner == '': banner = image
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': title, 'year' : year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    poster, banner = image, image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if action == 'shows_favourites':
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '2': cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'shows_subscriptions':
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_update)' % (sys.argv[0])))
                    cm.append((language(30426).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_clean)' % (sys.argv[0])))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                elif action.startswith('shows_search'):
                    cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows2&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s&imdb=%s&year=%s)' % (sys.argv[0], sysname, sysurl, sysimdb, sysyear)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s&year=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage, sysyear)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                if action == 'shows_search':
                    if ('"%s"' % url in favRead and '"%s"' % url in subRead): suffix = '|F|S| '
                    elif '"%s"' % url in favRead: suffix = '|F| '
                    elif '"%s"' % url in subRead: suffix = '|S| '
                    else: suffix = ''
                    name = suffix + name

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def seasonList(self, seasonList):
        if seasonList == None: return

        try:
            year, imdb, tvdb, genre, plot, show, show_alt = seasonList[0]['year'], seasonList[0]['imdb'], seasonList[0]['tvdb'], seasonList[0]['genre'], seasonList[0]['plot'], seasonList[0]['show'], seasonList[0]['show_alt']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                seasons = []
                for i in seasonList: seasons.append(i['season'])
                season_meta = metaget.get_seasons(show, imdb, seasons)
                meta = metaget.get_meta('tvshow', show, imdb_id=imdb)
                banner = meta['banner_url']
            else:
                meta = {'tvshowtitle': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                banner = ''
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(seasonList)
        for i in range(0, int(total)):
            try:
                name, url, image = seasonList[i]['name'], seasonList[i]['url'], seasonList[i]['image']
                sysname, sysurl, sysimage, sysyear, sysimdb, systvdb, sysgenre, sysplot, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show), urllib.quote_plus(show_alt)
                u = '%s?action=episodes&name=%s&url=%s&image=%s&year=%s&imdb=%s&tvdb=%s&genre=%s&plot=%s&show=%s&show_alt=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysyear, sysimdb, systvdb, sysgenre, sysplot, sysshow, sysshow_alt)

                if getSetting("meta") == 'true':
                    meta.update({'playcount': season_meta[i]['playcount'], 'overlay': season_meta[i]['overlay']})
                    poster = season_meta[i]['cover_url']
                    playcountMenu = language(30407).encode("utf-8")
                    if season_meta[i]['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason = urllib.quote_plus(re.sub('[^0-9]', '', str(season_meta[i]['imdb_id']))), urllib.quote_plus(str(season_meta[i]['season']))
                    if poster == '': poster = image
                    if banner == '': banner = poster
                    if banner == '': banner = image
                else:
                    poster, banner = image, image

                meta.update({'label': name, 'title': name, 'art(season.banner)': banner, 'art(season.poster': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                cm.append((language(30430).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        if episodeList == None: return

        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, year, imdb, tvdb, genre, plot, title, show, show_alt, season, episode = i['name'], i['url'], i['image'], i['date'], i['year'], i['imdb'], i['tvdb'], i['genre'], i['plot'], i['title'], i['show'], i['show_alt'], i['season'], i['episode']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(url)
                u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s&t=%s' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getSetting("meta") == 'true':
                    imdb = re.sub('[^0-9]', '', imdb)
                    meta = metaget.get_episode_meta(title, imdb, season, episode)
                    meta.update({'tvshowtitle': show})
                    if meta['title'] == '': meta.update({'title': title})
                    if meta['episode'] == '': meta.update({'episode': episode})
                    if meta['premiered'] == '': meta.update({'premiered': date})
                    if meta['plot'] == '': meta.update({'plot': plot})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason, metaepisode = urllib.quote_plus(re.sub('[^0-9]', '', str(meta['imdb_id']))), urllib.quote_plus(str(meta['season'])), urllib.quote_plus(str(meta['episode']))
                    label = str(meta['season']) + 'x' + '%02d' % int(meta['episode']) + ' . ' + meta['title']
                    if action == 'episodes_subscriptions': label = show + ' - ' + label
                    poster = meta['cover_url']
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'year' : year, 'premiered' : date, 'genre' : genre, 'plot': plot}
                    label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                    if action == 'episodes_subscriptions': label = show + ' - ' + label
                    poster = image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                if getSetting("autoplay") == 'true': cm.append((language(30432).encode("utf-8"), 'RunPlugin(%s?action=sources&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl)))
                else: cm.append((language(30433).encode("utf-8"), 'RunPlugin(%s?action=autoplay&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl)))
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s)' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl)))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                cm.append((language(30431).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def item_play_from_here(self, url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            i = str(i)
            label = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % i)
            if label == '': break

            params = {}
            path = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % i)
            path = urllib.quote_plus(path).replace('+%26+', '+&+')
            query = path.split('%3F', 1)[-1].split('%26')
            for i in query: params[urllib.unquote_plus(i).split('=')[0]] = urllib.unquote_plus(i).split('=')[1]
            sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl = urllib.quote_plus(params["name"]), urllib.quote_plus(params["title"]), urllib.quote_plus(params["imdb"]), urllib.quote_plus(params["tvdb"]), urllib.quote_plus(params["year"]), urllib.quote_plus(params["season"]), urllib.quote_plus(params["episode"]), urllib.quote_plus(params["show"]), urllib.quote_plus(params["show_alt"]), urllib.quote_plus(params["url"])
            u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=%s' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysurl)

            meta = {'title': xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'tvshowtitle': xbmc.getInfoLabel('ListItemNoWrap(%s).tvshowtitle' % i), 'season': xbmc.getInfoLabel('ListItemNoWrap(%s).season' % i), 'episode': xbmc.getInfoLabel('ListItemNoWrap(%s).episode' % i), 'writer': xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director': xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating': xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration': xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'premiered': xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'plot': xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i)}
            poster, fanart = xbmc.getInfoLabel('ListItemNoWrap(%s).icon' % i), xbmc.getInfoLabel('ListItemNoWrap(%s).Property(Fanart_Image)' % i)

            item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            item.setProperty("IsPlayable", "true")
            item.setProperty("Video", "true")
            item.setProperty("Fanart_Image", fanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            src = os.path.join(src, 'MyVideoNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            file = open(viewData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                if not line.startswith('"%s"|"%s"|"' % (skin, content)): file.write(line)
            file.write('"%s"|"%s"|"%s"\n' % (skin, content, str(view)))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url, image, imdb, year):
        try:
            index().container_refresh()
            file = open(data, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"|"%s"\n' % (name, year, imdb, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb, year):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            file = open(data, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"|"%s"\n' % (name, year, imdb, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(data, 'w')
            for line in list: file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            i = list.index(line)
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            i = list.index(line)
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

    def subscription_add(self, name, url, image, imdb, year):
        try:
            status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
            if status == 'Ended':
            	yes = index().yesnoDialog(language(30347).encode("utf-8"), language(30348).encode("utf-8"), name)
            	if not yes: return
            file = open(subData, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"|"%s"\n' % (name, year, imdb, url, image))
            file.close()
            self.library(name, url, imdb, year, silent=True)
            index().container_refresh()
            index().infoDialog(language(30312).encode("utf-8"), name)
        except:
            return

    def subscription_from_search(self, name, url, image, imdb, year):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30316).encode("utf-8"), name)
                return
            status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
            if status == 'Ended':
            	yes = index().yesnoDialog(language(30347).encode("utf-8"), language(30348).encode("utf-8"), name)
            	if not yes: return
            file = open(subData, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"|"%s"\n' % (name, year, imdb, url, image))
            file.close()
            self.library(name, url, imdb, year, silent=True)
            index().infoDialog(language(30312).encode("utf-8"), name)
        except:
            return

    def subscription_delete(self, name, url, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(subData, 'w')
            for line in list: file.write(line)
            file.close()

            yes = index().yesnoDialog(language(30351).encode("utf-8"), language(30352).encode("utf-8"), name)
            if yes:
                library = xbmc.translatePath(getSetting("tv_library"))
                enc_show = name.translate(None, '\/:*?"<>|')
                folder = os.path.join(library, enc_show)
                seasons = [os.path.join(folder, i) for i in xbmcvfs.listdir(folder)[0]]
                for season in seasons:
                    episodes = [os.path.join(season, i) for i in xbmcvfs.listdir(season)[1]]
                    for episode in episodes: xbmcvfs.delete(episode)
                    xbmcvfs.rmdir(season)
                xbmcvfs.rmdir(folder)

            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30313).encode("utf-8"), name)
        except:
            return

    def subscriptions_clean(self):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, imdb, url, image in match:
            	status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
            	if status == 'Ended':
            	    yes = index().yesnoDialog(language(30349).encode("utf-8"), language(30350).encode("utf-8"), name)
            	    if yes: self.subscription_delete(name, url, silent=True)
            index().container_refresh()
            index().infoDialog(language(30315).encode("utf-8"))
        except:
            return

    def subscriptions_update(self, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, year, imdb, url, image in match:
                if xbmc.abortRequested == True: sys.exit()
                self.library(name, url, imdb, year, silent=True)
            if getSetting("subscriptions_update") == 'true' and getSetting("subscriptions_updatelibrary") == 'true':
                xbmc.executebuiltin('UpdateLibrary(video)')
            if silent == False:
                index().infoDialog(language(30314).encode("utf-8"))
        except:
            return

    def metadata(self, content, imdb, season, episode):
        try:
            if content == 'movie' or content == 'tvshow':
                metaget.update_meta(content, '', imdb, year='')
                index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library(self, name, url, imdb, year, silent=False):
        try:
            library = xbmc.translatePath(getSetting("tv_library"))
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            show = name
            seasonList = seasons().get(url, '', year, imdb, '', '', show, idx=False)
            for i in seasonList:
                season, seasonUrl, tvdb, show_alt = i['name'], i['url'], i['tvdb'], i['show_alt']
                enc_show = show_alt.translate(None, '\/:*?"<>|')
                folder = os.path.join(library, enc_show)
                xbmcvfs.mkdir(folder)
                enc_season = season.translate(None, '\/:*?"<>|')
                seasonDir = os.path.join(folder, enc_season)
                xbmcvfs.mkdir(seasonDir)
                episodeList = episodes().get(season, seasonUrl, '', year, imdb, tvdb, '', '', show, show_alt, idx=False)
                for i in episodeList:
                    name, title, imdb, tvdb, year, season, episode, show, show_alt, date = i['name'], i['title'], i['imdb'], i['tvdb'], i['year'], i['season'], i['episode'], i['show'], i['show_alt'], i['date']
                    sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysdate = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt), urllib.quote_plus(date)
                    content = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&date=%s' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt, sysdate)
                    enc_name = name.translate(None, '\/:*?"<>|')
                    stream = os.path.join(seasonDir, enc_name + '.strm')
                    file = xbmcvfs.File(stream, 'w')
                    file.write(str(content))
                    file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), show)
        except:
            return

    def download(self, name, title, imdb, tvdb, year, season, episode, show, show_alt):
        try:
            property = (addonName+name)+'download'
            download = xbmc.translatePath(getSetting("downloads"))
            enc_name = name.translate(None, '\/:*?"<>|')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            file = [i for i in xbmcvfs.listdir(download)[1] if i.startswith(enc_name + '.')]
            if not file == []: file = os.path.join(download, file[0])
            else: file = None

            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return

            if file is None:
            	pass
            elif not file.endswith('.tmp'):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(file)
            	else:
            	    return
            elif file.endswith('.tmp'):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(file)

            url = resolver().run(name, title, imdb, tvdb, year, season, episode, show, show_alt, 'download://')
            if url is None: return
            url = url.rsplit('|', 1)[0]
            ext = url.rsplit('/', 1)[-1].rsplit('?', 1)[0].rsplit('|', 1)[0].strip().lower()
            ext = os.path.splitext(ext)[1][1:]
            if ext == '': ext = 'mp4'
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            request.add_header('Cookie', 'video=true')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def sources(self, name, title, imdb, tvdb, year, season, episode, show, show_alt):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'season': xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'director': xbmc.getInfoLabel('ListItem.director'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'premiered': xbmc.getInfoLabel('ListItem.premiered'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
        label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')

        sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt)
        u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=sources://' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt)

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        item.setProperty("IsPlayable", "true")
        item.setProperty("Video", "true")
        item.setProperty("Fanart_Image", fanart)
        xbmc.Player().play(u, item)

    def autoplay(self, name, title, imdb, tvdb, year, season, episode, show, show_alt):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'), 'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle'), 'season': xbmc.getInfoLabel('ListItem.season'), 'episode': xbmc.getInfoLabel('ListItem.episode'), 'writer': xbmc.getInfoLabel('ListItem.writer'), 'director': xbmc.getInfoLabel('ListItem.director'), 'rating': xbmc.getInfoLabel('ListItem.rating'), 'duration': xbmc.getInfoLabel('ListItem.duration'), 'premiered': xbmc.getInfoLabel('ListItem.premiered'), 'plot': xbmc.getInfoLabel('ListItem.plot')}
        label, poster, fanart = xbmc.getInfoLabel('ListItem.label'), xbmc.getInfoLabel('ListItem.icon'), xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')

        sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt = urllib.quote_plus(name), urllib.quote_plus(title), urllib.quote_plus(imdb), urllib.quote_plus(tvdb), urllib.quote_plus(year), urllib.quote_plus(season), urllib.quote_plus(episode), urllib.quote_plus(show), urllib.quote_plus(show_alt)
        u = '%s?action=play&name=%s&title=%s&imdb=%s&tvdb=%s&year=%s&season=%s&episode=%s&show=%s&show_alt=%s&url=play://' % (sys.argv[0], sysname, systitle, sysimdb, systvdb, sysyear, sysseason, sysepisode, sysshow, sysshow_alt)

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
        item.setInfo( type="Video", infoLabels= meta )
        item.setProperty("IsPlayable", "true")
        item.setProperty("Video", "true")
        item.setProperty("Fanart_Image", fanart)
        xbmc.Player().play(u, item)

class subscriptions:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(subData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': ''})
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def episodes(self):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()

            if read == '':
                index().okDialog(language(30323).encode("utf-8"), language(30324).encode("utf-8"))
            if not getSetting("subscriptions_update") == 'true':
                index().okDialog(language(30325).encode("utf-8"), language(30326).encode("utf-8"))

            imdbDict, seasons, episodes = {}, [], []
            library = xbmc.translatePath(getSetting("tv_library"))
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, year, imdb, url, image in match: imdbDict.update({imdb:image})
            shows = [os.path.join(library, i) for i in xbmcvfs.listdir(library)[0]]
            for show in shows: seasons += [os.path.join(show, i) for i in xbmcvfs.listdir(show)[0]]
            for season in seasons: episodes += [os.path.join(season, i) for i in xbmcvfs.listdir(season)[1] if i.endswith('.strm')]
        except:
            pass

        for episode in episodes:
            try:
                file = xbmcvfs.File(episode)
                read = file.read()
                read = read.encode("utf-8")
                file.close()
                if not read.startswith(sys.argv[0]): raise Exception()
                params = {}
                query = read[read.find('?') + 1:].split('&')
                for i in query: params[i.split('=')[0]] = i.split('=')[1]
                name, title, imdb, tvdb, year, season, episode, show, show_alt, date = urllib.unquote_plus(params["name"]), urllib.unquote_plus(params["title"]), urllib.unquote_plus(params["imdb"]), urllib.unquote_plus(params["tvdb"]), urllib.unquote_plus(params["year"]), urllib.unquote_plus(params["season"]), urllib.unquote_plus(params["episode"]), urllib.unquote_plus(params["show"]), urllib.unquote_plus(params["show_alt"]), urllib.unquote_plus(params["date"])
                image = imdbDict[imdb]
                sort = date.replace('-','')
                self.list.append({'name': name, 'url': name, 'image': image, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': '', 'plot': '', 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': episode, 'sort': sort})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        self.list = self.list[::-1][:100]

        index().episodeList(self.list)

class favourites:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, year, imdb, url, image in match:
            if getSetting("fav_sort") == '1':
                try: status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
                except: status = ''
            else:
                status = ''
            self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': '', 'plot': '', 'status': status})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))
        elif getSetting("fav_sort") == '1':
            filter = []
            self.list = sorted(self.list, key=itemgetter('name'))
            filter += [i for i in self.list if not i['status'] == 'Ended']
            filter += [i for i in self.list if i['status'] == 'Ended']
            self.list = filter

        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Episodes.png', 'action': 'episodes_subscriptions'})
        rootList.append({'name': 30502, 'image': 'Popular.png', 'action': 'shows_popular'})
        rootList.append({'name': 30503, 'image': 'Rating.png', 'action': 'shows_rating'})
        rootList.append({'name': 30504, 'image': 'Views.png', 'action': 'shows_views'})
        rootList.append({'name': 30505, 'image': 'Active.png', 'action': 'shows_active'})
        rootList.append({'name': 30506, 'image': 'Genres.png', 'action': 'genres_shows'})
        rootList.append({'name': 30507, 'image': 'Trakt.png', 'action': 'shows_trending'})
        rootList.append({'name': 30508, 'image': 'Favourites.png', 'action': 'shows_favourites'})
        rootList.append({'name': 30509, 'image': 'Subscriptions.png', 'action': 'shows_subscriptions'})
        rootList.append({'name': 30510, 'image': 'Search.png', 'action': 'shows_search'})
        index().rootList(rootList)
        index().downloadList()

class link:
    def __init__(self):
        self.imdb_base = 'http://www.imdb.com'
        self.imdb_akas = 'http://akas.imdb.com'
        self.imdb_title = 'http://www.imdb.com/title/tt%s/'
        self.imdb_genre = 'http://akas.imdb.com/genre/'
        self.imdb_genres = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&genres=%s'
        self.imdb_popular = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1'
        self.imdb_rating = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=user_rating,desc&count=25&start=1'
        self.imdb_views = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=num_votes,desc&count=25&start=1'
        self.imdb_active = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&production_status=active&sort=moviemeter,asc&count=25&start=1'
        self.imdb_search = 'http://akas.imdb.com/search/title?title_type=tv_series,mini_series&sort=moviemeter,asc&count=25&start=1&title=%s'

        self.tvdb_base = 'http://thetvdb.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.tvdb_series = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=tt%s&language=en'
        self.tvdb_series2 = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=en'
        self.tvdb_episodes = 'http://thetvdb.com/api/%s/series/%s/all/en.xml'
        self.tvdb_poster = 'http://thetvdb.com/banners/posters/'
        self.tvdb_thumb = 'http://thetvdb.com/banners/_cache/'

        self.trakt_base = 'http://api.trakt.tv'
        self.trakt_key = base64.urlsafe_b64decode('YmU2NDI5MWFhZmJiYmU2MmZkYzRmM2FhMGVkYjQwNzM=')
        self.trakt_summary = 'http://api.trakt.tv/show/summary.json/%s/%s'
        self.trakt_trending = 'http://api.trakt.tv/shows/trending.json/%s'

        self.tvrage_base = 'http://www.tvrage.com'
        self.tvrage_info = 'http://www.tvrage.com/feeds/full_show_info.php?sid=%s'

class genres:
    def __init__(self):
        self.list = []

    def imdb(self):
        #self.list = self.imdb_list()
        self.list = cache3(self.imdb_list)
        index().pageList(self.list)

    def imdb_list(self):
        try:
            result = getUrl(link().imdb_genre).result
            result = common.parseDOM(result, "div", attrs = { "class": "article" })
            result = [i for i in result if str('"tv_genres"') in i][0]
            genres = common.parseDOM(result, "td")
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                try: url = re.compile('genres=(.+?)&').findall(url)[0]
                except: url = re.compile('/genre/(.+?)/').findall(url)[0]
                url = link().imdb_genres % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonGenres.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class shows:
    def __init__(self):
        self.list = []

    def imdb(self, url):
        #self.list = self.imdb_list(url)
        self.list = cache(self.imdb_list, url)
        index().showList(self.list)
        index().nextList(self.list)

    def imdb_popular(self):
        #self.list = self.imdb_list(link().imdb_popular)
        self.list = cache(self.imdb_list, link().imdb_popular)
        index().showList(self.list)
        index().nextList(self.list)

    def imdb_rating(self):
        #self.list = self.imdb_list(link().imdb_rating)
        self.list = cache(self.imdb_list, link().imdb_rating)
        index().showList(self.list)
        index().nextList(self.list)

    def imdb_views(self):
        #self.list = self.imdb_list(link().imdb_views)
        self.list = cache(self.imdb_list, link().imdb_views)
        index().showList(self.list)
        index().nextList(self.list)

    def imdb_active(self):
        #self.list = self.imdb_list(link().imdb_active)
        self.list = cache(self.imdb_list, link().imdb_active)
        index().showList(self.list)
        index().nextList(self.list)

    def trakt_trending(self):
        #self.list = self.trakt_list(link().trakt_trending % link().trakt_key)
        self.list = cache(self.trakt_list, link().trakt_trending % link().trakt_key)
        index().showList(self.list)

    def imdb_search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.query = link().imdb_search % urllib.quote_plus(self.query)
            self.list = self.imdb_list(self.query)
            index().showList(self.list)

    def imdb_list(self, url):
        try:
            result = getUrl(url.replace(link().imdb_base, link().imdb_akas)).result
            result = result.decode('iso-8859-1').encode('utf-8')
            shows = common.parseDOM(result, "tr", attrs = { "class": ".+?" })
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "pagination" })[0]
            name = common.parseDOM(next, "a")[-1]
            if 'laquo' in name: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[-1]
            next = '%s%s' % (link().imdb_akas, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for show in shows:
            try:
                name = common.parseDOM(show, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = common.parseDOM(show, "span", attrs = { "class": "year_type" })[0]
                year = re.sub('[^0-9]', '', year)[:4]
                year = year.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (link().imdb_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')

                try:
                    image = common.parseDOM(show, "img", ret="src")[0]
                    if not ('._SX' in image or '._SY' in image): raise Exception()
                    image = image.rsplit('._SX', 1)[0].rsplit('._SY', 1)[0] + '._SX500.' + image.rsplit('.', 1)[-1] 
                except:
                    image = ''
                    meta = metaget.get_meta('tvshow', '', imdb_id=imdb)
                    image = meta['cover_url']
                    if not str(meta['year']) == year: image = ''
                    if not image == '': image = link().tvdb_poster + image.rsplit('\\', 1)[-1].rsplit('/', 1)[-1]
                if image == '': raise Exception()
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = common.parseDOM(show, "span", attrs = { "class": "genre" })
                    genre = common.parseDOM(genre, "a")
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = common.parseDOM(show, "span", attrs = { "class": "outline" })[0]
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

    def trakt_list(self, url):
        try:
            result = getUrl(url).result
            shows = json.loads(result)
        except:
            return

        for show in shows:
            try:
                name = show['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                year = show['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                imdb = show['imdb_id']
                imdb = re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')

                url = link().imdb_title % imdb
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = show['poster']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try:
                    genre = show['genres']
                    genre = " / ".join(genre)
                    genre = common.replaceHTMLCodes(genre)
                    genre = genre.encode('utf-8')
                except:
                    genre = ''

                try:
                    plot = show['overview']
                    plot = common.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except:
                    plot = ''

                self.list.append({'name': name, 'url': url, 'image': image, 'year': year, 'imdb': imdb, 'genre': genre, 'plot': plot})
            except:
                pass

        return self.list

class seasons:
    def __init__(self):
        self.list = []
        self.list2 = []

    def get(self, url, image, year, imdb, genre, plot, show, idx=True):
        if idx == True:
            #self.list = self.get_list(url, image, year, imdb, genre, plot, show)
            self.list = cache2(self.get_list, url, image, year, imdb, genre, plot, show)
            index().seasonList(self.list)
        else:
            self.list = self.get_list(url, image, year, imdb, genre, plot, show)
            return self.list

    def get_list(self, url, image, year, imdb, genre, plot, show):
        try:
            if imdb == '0': imdb = re.sub('[^0-9]', '', url.rsplit('tt', 1)[-1])

            try:
                result = getUrl(link().tvdb_series % imdb).result
                show_alt = common.parseDOM(result, "SeriesName")[0]
                tvdb = common.parseDOM(result, "seriesid")[0]
            except:
                result = getUrl(link().tvdb_series2 % urllib.quote_plus(show)).result
                result = common.parseDOM(result, "Series")
                result = [i for i in result if show == common.parseDOM(i, "SeriesName")[0] and year in common.parseDOM(i, "FirstAired")[0]][0]
                show_alt = common.parseDOM(result, "SeriesName")[0]
                tvdb = common.parseDOM(result, "seriesid")[0]

            show_alt = common.replaceHTMLCodes(show_alt)
            show_alt = show_alt.encode('utf-8')
            tvdb = common.replaceHTMLCodes(tvdb)
            tvdb = tvdb.encode('utf-8')

            threads = []
            threads.append(Thread(self.tvdb_list, url, image, year, imdb, tvdb, genre, plot, show, show_alt))
            threads.append(Thread(self.tvrage_list, url, image, year, imdb, tvdb, genre, plot, show, show_alt))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.list == None: self.list = []
            if self.list2 == None: self.list2 = []

            if len(self.list) == 0:
                return self.list2
            elif len(self.list2) > len(self.list):
                return self.list2
            elif any(len(i['season']) > 3 for i in self.list):
                return self.list2
            elif len(self.list) > 0:
                return self.list
        except:
            return

    def tvdb_list(self, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            result = getUrl(tvdbUrl).result

            seasons = common.parseDOM(result, "Episode")
            seasons = [i for i in seasons if common.parseDOM(i, "EpisodeNumber")[0] == '1']
            seasons = [i for i in seasons if not common.parseDOM(i, "SeasonNumber")[0] == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(season, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if int(date.replace('-','')) + 1 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d")): raise Exception()

                num = common.parseDOM(season, "SeasonNumber")[0]
                num = '%01d' % int(num)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list.append({'name': name, 'url': link().tvdb_base, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def tvrage_list(self, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            traktUrl = link().trakt_summary % (link().trakt_key, tvdb)
            result = getUrl(traktUrl).result
            result = json.loads(result)
            tvrage = result['tvrage_id']

            tvrageUrl = link().tvrage_info % tvrage
            result = getUrl(tvrageUrl).result

            seasons = common.parseDOM(result, "Season", ret="no")
            seasons = [i for i in seasons if not i == '0']
        except:
            return

        for season in seasons:
            try:
                date = common.parseDOM(result, "Season", attrs = { "no": season })[0]
                date = common.parseDOM(date, "airdate")[0]
                date = date.encode('utf-8')
                if int(date.replace('-','')) + 1 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d")): raise Exception()

                num = '%01d' % int(season)
                num = num.encode('utf-8')

                name = '%s %s' % ('Season', num)
                name = name.encode('utf-8')

                self.list2.append({'name': name, 'url': tvrageUrl, 'image': image, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': plot, 'show': show, 'show_alt': show_alt, 'season': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list2 = sorted(self.list2, key=itemgetter('sort'))
        return self.list2

class episodes:
    def __init__(self):
        self.list = []

    def get(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt, idx=True):
        if idx == True:
            #self.list = self.get_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
            self.list = cache(self.get_list, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
            index().episodeList(self.list)
        else:
            self.list = self.get_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
            return self.list

    def get_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        if url == link().tvdb_base:
            self.list = self.tvdb_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
        else:
            self.list = self.tvrage_list(name, url, image, year, imdb, tvdb, genre, plot, show, show_alt)
        return self.list

    def tvdb_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            tvdbUrl = link().tvdb_episodes % (link().tvdb_key, tvdb)
            result = getUrl(tvdbUrl).result

            episodes = common.parseDOM(result, "Episode")
            episodes = [i for i in episodes if '%01d' % int(common.parseDOM(i, "SeasonNumber")[0]) == season]
            episodes = [i for i in episodes if not common.parseDOM(i, "EpisodeNumber")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "FirstAired")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if int(date.replace('-','')) + 1 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d")): raise Exception()

                title = common.parseDOM(episode, "EpisodeName")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "EpisodeNumber")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                thumb = common.parseDOM(episode, "filename")[0]
                if not thumb == '': thumb = link().tvdb_thumb + thumb
                else: thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                try: desc = common.parseDOM(episode, "Overview")[0]
                except: desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

    def tvrage_list(self, name, url, image, year, imdb, tvdb, genre, plot, show, show_alt):
        try:
            season = re.sub('[^0-9]', '', name)
            season = season.encode('utf-8')

            result = getUrl(url).result
            episodes = common.parseDOM(result, "Season", attrs = { "no": season })[0]
            episodes = common.parseDOM(episodes, "episode")
            episodes = [i for i in episodes if not common.parseDOM(i, "seasonnum")[0] == '0']
        except:
            return

        for episode in episodes:
            try:
                date = common.parseDOM(episode, "airdate")[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')
                if int(date.replace('-','')) + 1 > int((datetime.datetime.utcnow() - datetime.timedelta(hours = 5)).strftime("%Y%m%d")): raise Exception()

                title = common.parseDOM(episode, "title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                num = common.parseDOM(episode, "seasonnum")[0]
                num = re.sub('[^0-9]', '', '%01d' % int(num))
                num = num.encode('utf-8')

                name = show_alt + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                try: thumb = common.parseDOM(episode, "screencap")[0]
                except: thumb = image
                thumb = common.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                desc = plot
                desc = common.replaceHTMLCodes(desc)
                desc = desc.encode('utf-8')

                self.list.append({'name': name, 'url': name, 'image': thumb, 'date': date, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'genre': genre, 'plot': desc, 'title': title, 'show': show, 'show_alt': show_alt, 'season': season, 'episode': num, 'sort': '%10d' % int(num)})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('sort'))
        return self.list

class resolver:
    def __init__(self):
        self.sources_dict()
        self.sources = []

    def run(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, url):
        try:
            self.sources = self.sources_get(name, title, imdb, tvdb, year, season, episode, show, show_alt, self.hostDict)
            self.sources = self.sources_filter()
            if self.sources == []: raise Exception()

            autoplay = getSetting("autoplay")
            if not xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
                autoplay = getSetting("autoplay_library")

            if url == 'play://':
                url = self.sources_direct()
            elif url == 'sources://' or url == 'download://' or not autoplay == 'true':
                url = self.sources_dialog()
            else:
                url = self.sources_direct()


            if url is None: raise Exception()
            if url == 'download://': return url
            if url == 'close://': return

            if getSetting("playback_info") == 'true':
                index().infoDialog(self.selectedSource, header=name)

            player().run(name, url, imdb)
            return url
        except:
            index().infoDialog(language(30318).encode("utf-8"))
            return

    def sources_get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        threads = []

        global watchseries_sources
        watchseries_sources = []
        threads.append(Thread(watchseries().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global tvonline_sources
        tvonline_sources = []
        if getSetting("tvonline") == 'true':
            threads.append(Thread(tvonline().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global vkbox_sources
        vkbox_sources = []
        if getSetting("vkbox") == 'true':
            threads.append(Thread(vkbox().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global istreamhd_sources
        istreamhd_sources = []
        if getSetting("istreamhd") == 'true':
            threads.append(Thread(istreamhd().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global simplymovies_sources
        simplymovies_sources = []
        if getSetting("simplymovies") == 'true':
            threads.append(Thread(simplymovies().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global watchmoviesonline_sources
        watchmoviesonline_sources = []
        if getSetting("watchonline") == 'true':
            threads.append(Thread(watchmoviesonline().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global moviestorm_sources
        moviestorm_sources = []
        if getSetting("moviestorm") == 'true':
            threads.append(Thread(moviestorm().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        global merdb_sources
        merdb_sources = []
        if getSetting("merdb") == 'true':
            threads.append(Thread(merdb().get, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict))

        [i.start() for i in threads]
        [i.join() for i in threads]

        self.sources = watchseries_sources + tvonline_sources + vkbox_sources + istreamhd_sources + simplymovies_sources + watchmoviesonline_sources + moviestorm_sources + merdb_sources

        return self.sources

    def sources_resolve(self, url, provider):
        try:
            if provider == 'Watchseries': url = watchseries().resolve(url)
            elif provider == 'TVonline': url = tvonline().resolve(url)
            elif provider == 'VKBox': url = vkbox().resolve(url)
            elif provider == 'iStreamHD': url = istreamhd().resolve(url)
            elif provider == 'Simplymovies': url = simplymovies().resolve(url)
            elif provider == 'Watchonline': url = watchmoviesonline().resolve(url)
            elif provider == 'Moviestorm': url = moviestorm().resolve(url)
            elif provider == 'MerDB': url = merdb().resolve(url)
            return url
        except:
            return

    def sources_filter(self):
        #host_rank = ['VKHD', 'WatchfreeinHD', 'TVonline', 'VK', 'Movreel', 'iShared', 'Putlocker', 'Sockshare', 'Flashx', 'Played', 'Vidx', 'Streamcloud']
        host_rank = [getSetting("hosthd1"), getSetting("hosthd2"), getSetting("host1"), getSetting("host2"), getSetting("host3"), getSetting("host4"), getSetting("host5"), getSetting("host6"), getSetting("host7"), getSetting("host8"), getSetting("host9"), getSetting("host10")]

        filter = []
        hosts = uniqueList(host_rank + sorted(self.hostDict.keys())).list
        for host in hosts: filter += [i for i in self.sources if i['source'] == host]
        self.sources = filter

        filter = [i for i in self.sources if i['quality'] == 'HD' and i['source'] in host_rank]
        filter += [i for i in self.sources if not i['quality'] == 'HD']
        self.sources = filter

        if not getSetting("quality") == 'true':
            self.sources = [i for i in self.sources if not i['quality'] == 'HD']

        count = 1
        for i in range(len(self.sources)):
            self.sources[i]['source'] = '#'+ str(count) + ' | ' + self.sources[i]['provider'].upper() + ' | ' + self.sources[i]['source'].upper() + ' | ' + self.sources[i]['quality']
            count = count + 1

        return self.sources

    def sources_dialog(self):
        try:
            sourceList, urlList, providerList = [], [], []

            for i in self.sources:
                sourceList.append(i['source'])
                urlList.append(i['url'])
                providerList.append(i['provider'])

            select = index().selectDialog(sourceList)
            if select == -1: return 'close://'

            url = self.sources_resolve(urlList[select], providerList[select])
            self.selectedSource = self.sources[select]['source']
            return url
        except:
            return

    def sources_direct(self):
        for i in self.sources:
            try:
                url = self.sources_resolve(i['url'], i['provider'])
                xbmc.sleep(1000)
                if url is None: raise Exception()
                self.selectedSource = i['source']
                return url
            except:
                pass

    def sources_dict(self):
        self.hostDict = {
        'VKHD': '.vk.me',
        'Muchmovies': 'muchmovies.org',
        'WatchfreeinHD': 'watchfreeinhd.com',
        'YIFY': 'yify.tv',

        '2gb-hosting': '2gb-hosting.com',
        'Allmyvideos': 'allmyvideos.net',
        #'180upload': '180upload.com',
        'Bayfiles': 'bayfiles.com',
        #'BillionUploads': 'billionuploads.com',
        'Castamp': 'castamp.com',
        #'Clicktoview': 'clicktoview.org',
        'Daclips': 'daclips.com',
        'Divxstage': 'divxstage.eu',
        'Donevideo': 'donevideo.com',
        'Ecostream': 'ecostream.tv',
        'Filenuke': 'filenuke.com',
        'Flashx': 'flashx.tv',
        'Gorillavid': 'gorillavid.com',
        'Hostingbulk': 'hostingbulk.com',
        #'Hugefiles': 'hugefiles.net',
        'iShared': 'ishared.eu',
        'Jumbofiles': 'jumbofiles.com',
        'Lemuploads': 'lemuploads.com',
        'Limevideo': 'limevideo.net',
        #'Megarelease': 'megarelease.org',
        'Mightyupload': 'mightyupload.com',
        'Movdivx': 'movdivx.com',
        'Movpod': 'movpod.net',
        'Movreel': 'movreel.com',
        'Movshare': 'movshare.net',
        'Movzap': 'movzap.com',
        'Muchshare': 'muchshare.net',
        'Nosvideo': 'nosvideo.com',
        'Novamov': 'novamov.com',
        'Nowvideo': 'nowvideo.co',
        'Played': 'played.to',
        'Playwire': 'playwire.com',
        'Primeshare': 'primeshare.tv',
        'Promptfile': 'promptfile.com',
        'Purevid': 'purevid.com',
        'Putlocker': 'putlocker.com',
        'Sharerepo': 'sharerepo.com',
        'Sharesix': 'sharesix.com',
        'Sockshare': 'sockshare.com',
        'StageVu': 'stagevu.com',
        'Streamcloud': 'streamcloud.eu',
        'Thefile': 'thefile.me',
        'TVonline': 'tvonline.cc',
        'Uploadc': 'uploadc.com',
        'Vidbull': 'vidbull.com',
        'Videobb': 'videobb.com',
        'Videoweed': 'videoweed.es',
        'Videozed': 'videozed.net',
        #'Vidhog': 'vidhog.com',
        #'Vidplay': 'vidplay.net',
        'Vidx': 'vidx.to',
        #'Vidxden': 'vidxden.com',
        'VK': '.vk.me',
        'Xvidstage': 'xvidstage.com',
        'Youwatch': 'youwatch.org',
        'Zalaa': 'zalaa.com'
        }


class watchseries:
    def __init__(self):
        self.watchseries_base = 'http://watchseries.lt'
        self.watchseries_search = 'http://watchseries.lt/search/%s'
        self.watchseries_episodes = 'http://watchseries.lt/episode/%s_s%s_e%s.html'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global watchseries_sources
            watchseries_sources = []

            query = self.watchseries_search % urllib.quote_plus(show)

            result = getUrl(query).result
            result = result.replace(' (%s)' % str(int(year) - 1), ' (%s)' % year)
            result = re.compile('href="(/serie/.+?)".+?[(]%s[)]' % year).findall(result)
            result = uniqueList(result).list

            match = [self.watchseries_base + i for i in result]
            if match == []: return
            for i in match[:5]:
                try:
                    result = getUrl(i).result
                    if any(x in self.cleantitle(result) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')]):
                        match2 = i
                    if str('tt' + imdb) in result:
                        match2 = i
                        break
                except:
                    pass
            url = match2.rsplit('/', 1)[-1]
            url = self.watchseries_episodes % (url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            for host in sorted(hostDict.keys()):
                try:
                    links = re.compile('<span>%s</span>.+?href="(.+?)"' % host.lower()).findall(result)
                    for url in links:
                        url = '%s%s' % (self.watchseries_base, url)
                        watchseries_sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchseries', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "a", ret="href", attrs = { "class": "myButton" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if url.startswith('http://ishared.eu'):
                result = getUrl(url).result
                url = re.compile('var xxxx = "(.+?)"').findall(result)[0]
                return url

            import urlresolver
            host = urlresolver.HostedMediaFile(url)
            if host: resolver = urlresolver.resolve(url)
            if not resolver.startswith('http://'): return
            if not resolver == url: return resolver
        except:
            return

class tvonline:
    def __init__(self):
        self.tvonline_base = 'http://tvonline.cc'
        self.tvonline_search = 'http://tvonline.cc/searchlist.php'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global tvonline_sources
            tvonline_sources = []

            query = self.tvonline_search
            post = 'keyword=%s' % urllib.quote_plus(show)

            result = getUrl(query, post=post).result
            result = common.parseDOM(result, "div", attrs = { "class": "tv_aes_l" })[0]
            result = common.parseDOM(result, "li")

            match = [i for i in result if any(x == self.cleantitle(common.parseDOM(i, "a")[-1]) for x in [self.cleantitle(show), self.cleantitle(show_alt)])]
            match2 = [self.tvonline_base + common.parseDOM(i, "a", ret="href")[-1] for i in match]
            if match2 == []: return
            for i in match2[:5]:
                try:
                    result = getUrl(i).result
                    match3 = common.parseDOM(result, "span", attrs = { "class": "years" })[0]
                    if any(x in match3 for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]):
                        match4 = result
                        break
                except:
                    pass

            result = common.parseDOM(match4, "li")
            try: match5 = [i for i in result if i.startswith('S%01d, Ep%02d:' % (int(season), int(episode)))][0]
            except: pass
            try: match5 = [i for i in result if str('>' + self.cleantitle(title) + '<') in self.cleantitle(i)][0]
            except: pass
            url = common.parseDOM(match5, "a", ret="href")[0]
            url = '%s%s' % (self.tvonline_base, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            tvonline_sources.append({'source': 'TVonline', 'quality': 'SD', 'provider': 'TVonline', 'url': url})
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            self.login_link = 'http://tvonline.cc/login.php'
            self.reg_link = 'http://tvonline.cc/reg.php'
            self.key_link = base64.urlsafe_b64decode('X21ldGhvZD1QT1NUJiVzPWxvZ2luJlVzZXJVc2VybmFtZT1hOTQ2ODUxJnN1YnNjcmlwdGlvbnNQYXNzPWE5NDY4NTE=')
            self.video_link = 'http://tvonline.cc/play.php?id=nktlltn-ekkn'

            result = getUrl(self.reg_link, close=False).result
            post = re.compile('name="(Token.+?)" value=".+?"').findall(result)[0]
            post = self.key_link % post

            result = getUrl(self.reg_link, post=post, referer=self.login_link, close=False).result
            result = getUrl(self.video_link).result
            result = common.parseDOM(result, "video", ret="src", attrs = { "id": "ipadvideo" })[0]
            key5 = re.compile('key=\w*-(\w{5})').findall(result)[0]
            dom = re.compile('//(.+?)[.]').findall(result)[0]

            import random
            splitkey = url.split('?id=')[-1].split('-')
            key1 = splitkey[0]
            key4 = splitkey[1]
            keychar = "beklm"
            key_length = 3
            key2 = ""
            for i in range(key_length):
                next_index = random.randrange(len(keychar))
                key2 = key2 + keychar[next_index]

            keychar = "ntwyz"
            key_length = 3
            key3 = ""
            for i in range(key_length):
                next_index = random.randrange(len(keychar))
                key3 = key3 + keychar[next_index]# friday k saturday w sunday z

            url = 'http://%s.tvonline.cc/ip.mp4?key=%s-%s%s%s-%s' % (dom,key1,key5, key2, key3, key4)
            return url
        except:
            return


class vkbox:
    def __init__(self):
        self.mobapps_base = 'http://mobapps.cc'
        self.mobapps_data = 'http://mobapps.cc/data/data_en.zip'
        self.mobapps_episodes = 'http://mobapps.cc/api/serials/e/?h=%s&u=%s&y=%s'
        self.mobapps_tv = 'tv_lite.json'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global vkbox_sources
            vkbox_sources = []

            search = 'http://www.imdbapi.com/?i=tt%s' % imdb
            search = getUrl(search).result
            search = json.loads(search)
            country = search['Country']
            if not 'USA' in country: return

            #result = self.getdata()
            result = cache2(self.getdata)
            result = json.loads(result)

            match = [i['id'] for i in result if any(x == self.cleantitle(i['title']) for x in [self.cleantitle(show), self.cleantitle(show_alt)])][0]
            url = self.mobapps_episodes % (match, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            request = urllib2.Request(url,None)
            request.add_header('User-Agent', 'android-async-http/1.4.1 (http://loopj.com/android-async-http)')
            response = urllib2.urlopen(request, timeout=10)
            result = response.read()
            response.close()
            param = re.findall('"lang":"en","apple":(\d+?),"google":(\d+?),"microsoft":"(.+?)"', result, re.I)
            num = int(match) + int(season) + int(episode)
            url = 'https://vk.com/video_ext.php?oid=%s&id=%s&hash=%s' % (str(int(param[0][0]) + num), str(int(param[0][1]) + num), param[0][2])

            result = getUrl(url).result
            try:
                url = re.compile('url720=(.+?)&').findall(result)[0]
                vkbox_sources.append({'source': 'VKHD', 'quality': 'HD', 'provider': 'VKBox', 'url': url})
            except:
                pass
            try:
                url = re.compile('url540=(.+?)&').findall(result)[0]
                vkbox_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'VKBox', 'url': url})
            except:
                pass
            try:
                url = re.compile('url480=(.+?)&').findall(result)[0]
                vkbox_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'VKBox', 'url': url})
            except:
                pass
        except:
            return

    def getdata(self):
        try:
            import zipfile, StringIO
            data = urllib2.urlopen(self.mobapps_data, timeout=10).read()
            zip = zipfile.ZipFile(StringIO.StringIO(data))
            read = zip.open(self.mobapps_tv)
            result = read.read()
            return result
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class istreamhd:
    def __init__(self):
        self.istreamhd_base = 'http://istreamhd.org'
        self.istreamhd_get = 'http://istreamhd.org/get'
        self.istreamhd_search = 'http://istreamhd.org/get/mini_search.php?&count=10&q=%s'
        self.istreamhd_watch = 'http://istreamhd.org//lib/get_embed.php?%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global istreamhd_sources
            istreamhd_sources = []

            query = self.istreamhd_search % (urllib.quote_plus(show))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "ui-block.+?" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s%s' % (self.istreamhd_base, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile('(>Season %s<.+)' % season).findall(result)[0]
            url = url.split('"list-divider"', 1)[0]
            url = re.compile('(.+ E%s</a>)' % episode).findall(url)[0]
            url = url.split(" E%s</a>" % episode, 1)[0]
            url = common.parseDOM(url, "a", ret="href")[-1]
            if not url.startswith('item.php'): raise Exception()
            url = '%s/%s' % (self.istreamhd_get, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile('/lib/get_embed.php.+?"(.+?)"').findall(result)[0]
            url = self.istreamhd_watch % url
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            result = getUrl(url).result
            try:
                url = re.compile('url720=(.+?)&').findall(result)[0]
                istreamhd_sources.append({'source': 'VKHD', 'quality': 'HD', 'provider': 'iStreamHD', 'url': url})
            except:
                pass
            try:
                url = re.compile('url540=(.+?)&').findall(result)[0]
                istreamhd_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'iStreamHD', 'url': url})
            except:
                pass
            try:
                url = re.compile('url480=(.+?)&').findall(result)[0]
                istreamhd_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'iStreamHD', 'url': url})
            except:
                pass
        except:
            return

    def resolve(self, url):
        return url

class simplymovies:
    def __init__(self):
        self.simplymovies_base = 'http://simplymovies.net'
        self.simplymovies_search = 'http://simplymovies.net/tv_shows.php?searchTerm='

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global simplymovies_sources
            simplymovies_sources = []

            query = self.simplymovies_search + urllib.quote_plus(show.replace(' ', '-'))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
            try: match = [i for i in url if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')])][0]
            except: pass
            try: match = [i for i in url if str('tt' + imdb) in i][0]
            except: pass
            url = common.parseDOM(match, "a", ret="href")[0]
            url = '%s/%s' % (self.simplymovies_base, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = re.compile('<h3>(Season %s<.+)' % season).findall(result)[0]
            url = url.split("<h3>")[0]
            url = url.replace(':','<')
            url = re.compile('(.+>Episode %s<)' % episode).findall(url)[0]
            url = re.compile('"(.+?)"').findall(url)[-1]
            url = '%s/%s' % (self.simplymovies_base, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            result = getUrl(url).result
            try:
                url = re.compile('url720=(.+?)&').findall(result)[0]
                simplymovies_sources.append({'source': 'VKHD', 'quality': 'HD', 'provider': 'Simplymovies', 'url': url})
            except:
                pass
            try:
                url = re.compile('url540=(.+?)&').findall(result)[0]
                simplymovies_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'Simplymovies', 'url': url})
            except:
                pass
            try:
                url = re.compile('url480=(.+?)&').findall(result)[0]
                simplymovies_sources.append({'source': 'VK', 'quality': 'SD', 'provider': 'Simplymovies', 'url': url})
            except:
                pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        return url

class watchmoviesonline:
    def __init__(self):
        self.watchmoviesonline_base = 'http://watchmoviesonline.mobi'
        self.watchmoviesonline_search = 'http://watchmoviesonline.mobi/?movieorserie=1&search='
        self.watchmoviesonline_episodes = 'http://watchmoviesonline.mobi/title/%s?m=%s&s=%s&e=%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global watchmoviesonline_sources
            watchmoviesonline_sources = []

            query = self.watchmoviesonline_search + urllib.quote_plus(show)

            result = getUrl(query).result
            result = common.parseDOM(result, "div", attrs = { "class": "rowcol.+?" })

            match = [i for i in result if any(x in self.cleantitle(i) for x in [str('>' + self.cleantitle(show) + '<'), str('>' + self.cleantitle(show_alt) + '<')])]
            match2 = [self.watchmoviesonline_base + re.compile('"(/title/.+?)"').findall(i)[0] for i in match]
            if match2 == []: return
            for i in match2[:5]:
                try:
                    result = getUrl(i).result
                    match3 = re.compile('[(](\d{4})[)]').findall(result)[0]
                    if any(x == match3 for x in [str(year), str(int(year)+1), str(int(year)-1)]):
                        match4 = i
                        break
                except:
                    pass
            url = match4.split('/title/', 1)[-1].split('/', 1)[0]
            url = self.watchmoviesonline_episodes % (url, url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')

            for v1, v2  in re.compile("return p}[(]'(.+?);',.+?,.+?,'(.+?)'.split").findall(result):
                try:
                    v2 = v2.split('|')
                    for i in range(len(v2)):
                        if v2[i]: v1 = re.sub('\\b%s\\b' % self.base36encode(i), v2[i], v1)
                    url = base64.b64decode(v1.split('"')[1])
                    url = common.parseDOM(url, "a")[0]
                    for host in sorted(hostDict.keys()):
                        if 'watchfreeinhd.com' in url:
                            watchmoviesonline_sources.append({'source': 'WatchfreeinHD', 'quality': 'HD', 'provider': 'Watchonline', 'url': url})
                            break
                        elif hostDict[host] in url:
                            watchmoviesonline_sources.append({'source': host, 'quality': 'SD', 'provider': 'Watchonline', 'url': url})
                except:
                    pass
        except:
            return

    def base36encode(self, number):
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
        if number < 0:
            raise ValueError('number must be positive')

        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        base36 = ''
        while number:
            number, i = divmod(number, 36)
            base36 = alphabet[i] + base36

        return base36 or alphabet[0]

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            import urlresolver
            host = urlresolver.HostedMediaFile(url)
            if host: resolver = urlresolver.resolve(url)
            if not resolver.startswith('http://'): return
            if not resolver == url: return resolver
        except:
            return

class moviestorm:
    def __init__(self):
        self.moviestorm_base = 'http://moviestorm.eu'
        self.moviestorm_search = 'http://moviestorm.eu/search?q=%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global moviestorm_sources
            moviestorm_sources = []

            query = self.moviestorm_search % (urllib.quote_plus(show))

            result = getUrl(query).result
            url = common.parseDOM(result, "div", attrs = { "class": "movie_box" })
            url = [i for i in url if str('tt' + imdb) in i][0]
            url = common.parseDOM(url, "a", ret="href")[0]
            url = '%s?season=%s&episode=%s' % (url, season, episode)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "searialinks" })[0]
            links = re.compile('"(http://ishared.eu/.+?)"').findall(result)

            for url in links:
                moviestorm_sources.append({'source': 'iShared', 'quality': 'SD', 'provider': 'Moviestorm', 'url': url})
        except:
            return

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('var xxxx = "(.+?)"').findall(result)[0]
            return url
        except:
            return

class merdb:
    def __init__(self):
        self.merdb_base = 'http://www.merdb.ru'
        self.merdb_search = 'http://www.merdb.ru/tvshow/?search=%s'

    def get(self, name, title, imdb, tvdb, year, season, episode, show, show_alt, hostDict):
        try:
            global merdb_sources
            merdb_sources = []

            query = self.merdb_search % (urllib.quote_plus(show))

            result = getUrl(query).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "list_box_title" })

            match = [i for i in result if any(x == self.cleantitle(common.parseDOM(i, "a", ret="title")[0]) for x in [self.cleantitle(show), self.cleantitle(show_alt)])]
            match2 = [i for i in match if any(x in common.parseDOM(i, "a")[0] for x in ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)])][0]
            url = common.parseDOM(match2, "a", ret="href")[0]
            url = '%s%s' % (self.merdb_base, url)
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "tv_container" })[0]
            url = common.parseDOM(result, "a", ret="href")[0]
            url = url.rsplit('/season', 1)[0]
            url = '%s%s/season-%01d-episode-%01d' % (self.merdb_base, url, int(season), int(episode))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            result = result.replace('\n','')
            links = re.compile('(<a href="/external.php.+?".+?</script>)').findall(result)
            for host in sorted(hostDict.keys()):
                try:
                    links_match = [i for i in links if "document.writeln('%s." % host.lower() in i]
                    for url in links_match:
                        url = common.parseDOM(url, "a", ret="href")[0]
                        url = '%s%s' % (self.merdb_base, url)
                        url = common.replaceHTMLCodes(url)
                        url = url.encode('utf-8')
                        merdb_sources.append({'source': host, 'quality': 'SD', 'provider': 'MerDB', 'url': url})
                except:
                    pass
        except:
            return

    def cleantitle(self, title):
        title = re.sub('\n|\s(|[(])(UK|US|AU)(|[)])$|\s(vs|v[.])\s|(:|;|-|"|,|\'|\.|\?)|\s', '', title).lower()
        return title

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-1').encode('utf-8')
            url = common.parseDOM(result, "frame", ret="src", attrs = { "id": "play_bottom" })[0]
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            if url.startswith('http://ishared.eu'):
                result = getUrl(url).result
                url = re.compile('var xxxx = "(.+?)"').findall(result)[0]
                return url

            import urlresolver
            host = urlresolver.HostedMediaFile(url)
            if host: resolver = urlresolver.resolve(url)
            if not resolver.startswith('http://'): return
            if not resolver == url: return resolver
        except:
            return


main()