import { useState, useEffect } from 'react'
import {
  PlayIcon,
  PauseIcon,
  ForwardIcon,
  BackwardIcon,
  PlusIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  MusicalNoteIcon,
  QueueListIcon,
} from '@heroicons/react/24/solid'

interface Track {
  id: number
  path: string
  title: string
  artist: string
  album: string
  tracknumber: number
  duration: number
}

type View = 'tracks' | 'albums'

function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function groupByAlbum(tracks: Track[]): Record<string, Track[]> {
  return tracks.reduce((groups, track) => {
    const album = track.album || 'Unknown Album'
    if (!groups[album]) groups[album] = []
    groups[album].push(track)
    return groups
  }, {} as Record<string, Track[]>)
}

function App() {
  const [library, setLibrary] = useState<Track[]>([])
  const [queue, setQueue] = useState<Track[]>([])
  const [isPlaying, setIsPlaying] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [view, setView] = useState<View>('tracks')

  useEffect(() => {
    fetchLibrary()
  }, [])

  async function fetchLibrary() {
    const res = await fetch('/api/library')
    const data = await res.json()
    setLibrary(data)
  }

  async function search(q: string) {
    setSearchQuery(q)
    if (q.trim() === '') {
      fetchLibrary()
      return
    }
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`)
    const data = await res.json()
    setLibrary(data)
  }

  async function addToQueue(track: Track) {
    await fetch('/api/queue/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(track),
    })
    refreshQueue()
  }

  async function refreshQueue() {
    const res = await fetch('/api/queue')
    const data = await res.json()
    setQueue(data)
  }

  async function play() {
    await fetch('/api/play', { method: 'POST' })
    setIsPlaying(true)
  }

  async function pause() {
    await fetch('/api/pause', { method: 'POST' })
    setIsPlaying(false)
  }

  async function next() {
    await fetch('/api/next', { method: 'POST' })
  }

  async function previous() {
    await fetch('/api/prev', { method: 'POST' })
  }

  async function clearQueue() {
    await fetch('/api/queue/clear', { method: 'POST' })
    setQueue([])
    setIsPlaying(false)
  }

  function handlePlayPause() {
    if (!isPlaying) {
      if (queue.length > 0) play()
    } else {
      pause()
    }
  }

  const sortedTracks = [...library].sort((a, b) => a.title.localeCompare(b.title))

  const albumGroups = groupByAlbum(library)
  const sortedAlbums = Object.keys(albumGroups).sort((a, b) => a.localeCompare(b))

  return (
    <div className="h-screen bg-[#0F0F0F] text-[#EDEDED] flex flex-col">

      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-[#2A2A2A]">
        <div className="flex items-center gap-2">
          <MusicalNoteIcon className="w-6 h-6 text-purple-400" />
          <h1 className="text-xl font-semibold tracking-wide text-white">PRISM</h1>
        </div>
        <div className="relative">
          <MagnifyingGlassIcon className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#A0A0A0]" />
          <input
            type="text"
            placeholder="Search tracks, artists, albums..."
            value={searchQuery}
            onChange={(e) => search(e.target.value)}
            className="bg-[#1A1A1A] border border-[#2A2A2A] rounded-lg pl-9 pr-4 py-2 text-sm text-[#EDEDED] placeholder-[#A0A0A0] focus:outline-none focus:border-purple-500 w-80"
          />
        </div>
      </header>

      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">

        {/* Library */}
        <div className="flex-1 overflow-y-auto p-6">

          {/* Library header with view toggle */}
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-[#A0A0A0] uppercase tracking-wider">Library</h2>
            <div className="flex items-center bg-[#1A1A1A] rounded-lg p-1 gap-1">
              <button
                onClick={() => setView('tracks')}
                className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                  view === 'tracks'
                    ? 'bg-[#2A2A2A] text-[#EDEDED]'
                    : 'text-[#A0A0A0] hover:text-[#EDEDED]'
                }`}
              >
                Tracks
              </button>
              <button
                onClick={() => setView('albums')}
                className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                  view === 'albums'
                    ? 'bg-[#2A2A2A] text-[#EDEDED]'
                    : 'text-[#A0A0A0] hover:text-[#EDEDED]'
                }`}
              >
                Albums
              </button>
            </div>
          </div>

          {/* Tracks view */}
          {view === 'tracks' && (
            <div className="space-y-1">
              {sortedTracks.map((track) => (
                <div
                  key={track.id}
                  onDoubleClick={() => addToQueue(track)}
                  className="flex items-center justify-between px-4 py-3 rounded-lg hover:bg-[#1A1A1A] group transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-4 min-w-0">
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-[#EDEDED] truncate">{track.title}</p>
                      <p className="text-xs text-[#A0A0A0] truncate">{track.artist} · {track.album}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs text-[#A0A0A0]">{formatDuration(track.duration)}</span>
                    <button
                      onClick={() => addToQueue(track)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-[#2A2A2A]"
                    >
                      <PlusIcon className="w-4 h-4 text-purple-400" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Albums view */}
          {view === 'albums' && (
            <div className="space-y-6">
              {sortedAlbums.map((albumName) => {
                const tracks = albumGroups[albumName].sort((a, b) => a.tracknumber - b.tracknumber)
                return (
                  <div key={albumName}>
                    <div className="mb-2 px-4">
                      <p className="text-sm font-semibold text-[#EDEDED]">{albumName}</p>
                      <p className="text-xs text-[#A0A0A0]">{tracks[0].artist}</p>
                    </div>
                    <div className="space-y-1">
                      {tracks.map((track) => (
                        <div
                          key={track.id}
                          onDoubleClick={() => addToQueue(track)}
                          className="flex items-center justify-between px-4 py-2 rounded-lg hover:bg-[#1A1A1A] group transition-colors cursor-pointer"
                        >
                          <div className="flex items-center gap-4 min-w-0">
                            <span className="text-[#A0A0A0] text-xs w-5 text-right shrink-0">{track.tracknumber}</span>
                            <p className="text-sm text-[#EDEDED] truncate">{track.title}</p>
                          </div>
                          <div className="flex items-center gap-3 shrink-0">
                            <span className="text-xs text-[#A0A0A0]">{formatDuration(track.duration)}</span>
                            <button
                              onClick={() => addToQueue(track)}
                              className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-[#2A2A2A]"
                            >
                              <PlusIcon className="w-4 h-4 text-purple-400" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          )}

        </div>

        {/* Divider */}
        <div className="w-px bg-[#2A2A2A]" />

        {/* Queue */}
        <div className="w-80 overflow-y-auto p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <QueueListIcon className="w-4 h-4 text-[#A0A0A0]" />
              <h2 className="text-sm font-semibold text-[#A0A0A0] uppercase tracking-wider">Queue</h2>
              <span className="text-xs text-[#A0A0A0]">({queue.length})</span>
            </div>
            {queue.length > 0 && (
              <button onClick={clearQueue} className="p-1 rounded hover:bg-[#1A1A1A] transition-colors">
                <TrashIcon className="w-4 h-4 text-[#A0A0A0] hover:text-red-400" />
              </button>
            )}
          </div>
          <div className="space-y-1">
            {queue.length === 0 ? (
              <p className="text-sm text-[#A0A0A0] text-center mt-8">Queue is empty</p>
            ) : (
              queue.map((track, index) => (
                <div key={index} className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-[#1A1A1A] transition-colors">
                  <span className="text-xs text-[#A0A0A0] w-4 shrink-0">{index + 1}</span>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-[#EDEDED] truncate">{track.title}</p>
                    <p className="text-xs text-[#A0A0A0] truncate">{track.artist}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Playback bar */}
      <div className="border-t border-[#2A2A2A] bg-[#1A1A1A] px-6 py-4 flex items-center justify-center gap-6">
        <button onClick={previous} className="p-2 rounded-full hover:bg-[#2A2A2A] transition-colors">
          <BackwardIcon className="w-5 h-5 text-[#EDEDED]" />
        </button>
        <button onClick={handlePlayPause} className="p-3 rounded-full bg-purple-500 hover:bg-purple-400 transition-colors">
          {isPlaying
            ? <PauseIcon className="w-5 h-5 text-white" />
            : <PlayIcon className="w-5 h-5 text-white" />
          }
        </button>
        <button onClick={next} className="p-2 rounded-full hover:bg-[#2A2A2A] transition-colors">
          <ForwardIcon className="w-5 h-5 text-[#EDEDED]" />
        </button>
      </div>

    </div>
  )
}

export default App
