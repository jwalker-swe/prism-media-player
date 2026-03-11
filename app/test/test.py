from app.library.metadata import extract_metadata


path = "/Users/jordan/Music/library/tyler_the_creator/dont_tap_the_glass/01.flac"

data = extract_metadata(path)

print(data)
