"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ImportError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Sample user preference profiles
    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {profile_name} ===")
        print("Top recommendations:\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} — Score: {score:.2f}")
            print(f"   Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
