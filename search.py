
import asyncio
import json

from pytok.tiktok import PyTok

hashtag_name = 'bakla ampota'

async def main():
    async with PyTok(manual_captcha_solves=True) as api:
        search = api.search(hashtag_name)

        videos = []
        async for video in search.videos(count=1000):
            video_info = await video.info()
            try:
                print(video_info["music"]["playUrl"])
                videos.append(video_info["music"]["playUrl"])
            except KeyError:
                print("No music found for this video.")
                continue
        
        print(len(videos))

        with open("outs/"+hashtag_name+".json", "w") as out_file:
            json.dump(videos, out_file)

if __name__ == "__main__":
    asyncio.run(main())