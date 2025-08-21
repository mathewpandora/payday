from content_generation.video_generator.runway_video_generator import RunwayVideoGenerator
from dotenv import load_dotenv

load_dotenv()


client = RunwayVideoGenerator()



video_url, filepath = client.generate_scene_and_video("evil clown standing in the circus with knife and and he has a sarcastic smile", "the clown begins to run in a circle after his victim who entered the circus. She was the first visitor. The clown begins to chase her with a knife, having reached the goal he dissolves", duration=10)

print(video_url)