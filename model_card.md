# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeDetector**  

---

## 2. Intended Use  

This recommender generates a ranked top-5 list of songs from a fixed 18-song catalog by scoring each song against a user's stated preferences (favorite genre, favorite mood, target energy level, and whether they like acoustic tracks), then explaining each recommendation with the specific reasons it scored well. It assumes the user can articulate their taste as a few discrete, well-formed inputs — an exact genre label, an exact mood label, and a numeric energy target between 0 and 1 — rather than inferring taste from listening history or implicit signals, and it assumes those inputs are typed consistently (e.g., matching the catalog's casing) since matching is currently exact-string rather than fuzzy. This is a classroom exploration of recommender-system mechanics, not a production system: the catalog is small and hand-curated, several biases and edge-case bugs remain (see Sections 6–7), and it's meant to teach how simple weighted scoring, explanation generation, and evaluation work rather than to serve real listeners.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.) 

    Genre
    Mood
    Energy
    Acousticness (via the likes_acoustic flag)

- What user preferences are considered  

    Favorite genre
    Favorite mood
    Target energy
    Whether they like acoustic songs (likes_acoustic)

- How does the model turn those into a score

    Each song starts at 0 and earns points for matching the user's preferences: +2 for an exact genre match, +1 for an exact mood match, up to +1 for how close the song's energy is to the user's target energy (closer = more points, linearly), and +0.5 if the user likes acoustic songs and the song is acoustic (acousticness > 0.5). The song's total score determines its rank.

- What changes did you make from the starter logic  

    I filled in the actual logic: writing the part that reads all the songs in from the spreadsheet file, writing the actual scoring rules (giving points for matching genre, mood, energy closeness, and acoustic preference), and writing the part that takes all those scores and sorts the songs into a ranked top-5 list with a plain-English explanation for each pick.

---

## 4. Data  

The dataset is a fixed catalog of 18 songs each with a title, artist, genre, mood, and several numeric attributes (energy, tempo, valence, danceability, acousticness). I only added data and never really removed any data and of course there would be a gap  of musical taste missing in the dataset due to how small the dataset is.

---

## 5. Strengths  

Where does your system seem to work well  

The system works best for users whose favorite genre and mood happen to align with the same song, and whose target energy is near the catalog's high or low clusters (0.25–0.42 or 0.75–0.97) rather than the sparse middle band. The scoring also correctly captures the intuition that an exact genre or mood match should count for more than a rough energy match, and that a song satisfying multiple preferences at once should clearly outrank one satisfying only a single preference. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The scoring never looks at tempo, valence, or danceability — a user who wants something upbeat and danceable but doesn't fit a specific genre/mood label has no way to express that, since those columns are loaded but never used. Genre and mood coverage is extremely thin: 13 of 15 genres and most moods have exactly one song each, so users whose favorite genre falls outside "pop" or "lofi" always get the same single song recommended regardless of fit on other axes — there's no real competition for that slot. The system also overfits hard to genre: because it's worth +2.0 (the largest single weight), any exact genre match can outrank a song that's a better overall fit on mood and energy but doesn't share genre, and combined with the 1-song-per-genre problem this means genre match alone frequently decides the outcome. Scoring also unintentionally favors users whose energy target lands near the catalog's dense clusters over users with a genuinely moderate energy preference since almost no songs live in that middle band — and it favors users who type genre/mood in the exact casing used by the CSV, since matching is case-sensitive and a user typing "Pop" instead of "pop" loses the full genre-match points even on an otherwise perfect fit.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Besides the 3 sample profiles in `main.py`, I ran 8 adversarial profiles (see below) covering conflicting preferences, nonexistent genres, out-of-range/negative energy, an acoustic-only "freebie," an all-`None` profile, a case mismatch, and a tie-prone lofi query. For each, I checked whether the score breakdown matched the math and whether the top result made intuitive sense. The most surprising result: typing `"Pop"`/`"Happy"` instead of `"pop"`/`"happy"` matched nothing, even though a perfect-fit song existed — it only showed up in the top 5 by luck. I also confirmed `target_energy` isn't clamped to `[0,1]`, so out-of-range values silently produce meaningless energy scores instead of an error.

### Adversarial / edge-case profiles

To probe whether `score_song` could be tricked, I ran 8 adversarial user profiles against `data/songs.csv` and inspected the top-5 recommendations for each.

**1. Conflicting signals (high energy + sad mood)** — `{"genre": "rock", "mood": "sad", "energy": 0.9}`

```
1. Storm Runner by Voltline — Score: 2.99
   Because: genre match (+2.0), energy similarity (+0.99)
2. Gym Hero by Max Pulse — Score: 0.97
   Because: energy similarity (+0.97)
3. Pulse Overdrive by Kilowatt — Score: 0.95
   Because: energy similarity (+0.95)
4. Iron Descent by Graveyard Chorus — Score: 0.93
   Because: energy similarity (+0.93)
5. Sunrise City by Neon Echo — Score: 0.92
   Because: energy similarity (+0.92)
```

Genre match dominated the mismatched "sad" mood as expected — no bug, but shows genre currently outweighs mood by 2x.

**2. Impossible genre/mood** — `{"genre": "polka", "mood": "ecstatic", "energy": 0.5}`

```
1. Velvet Whispers by Honey Marlowe — Score: 0.98
   Because: energy similarity (+0.98)
2. Dusty Backroads by Sable & Wren — Score: 0.95
   Because: energy similarity (+0.95)
3. Island Sway by Cool Tide Collective — Score: 0.92
   Because: energy similarity (+0.92)
4. Midnight Coding by LoRoom — Score: 0.92
   Because: energy similarity (+0.92)
5. Focus Flow by LoRoom — Score: 0.90
   Because: energy similarity (+0.90)
```

Gracefully degrades to energy-only ranking, no crash.

**3. Out-of-range energy (1.5)** — `{"genre": "pop", "mood": "happy", "energy": 1.5}`

```
1. Sunrise City by Neon Echo — Score: 3.32
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.32)
2. Gym Hero by Max Pulse — Score: 2.43
   Because: genre match (+2.0), energy similarity (+0.43)
3. Rooftop Lights by Indigo Parade — Score: 1.26
   Because: mood match (+1.0), energy similarity (+0.26)
4. Iron Descent by Graveyard Chorus — Score: 0.47
   Because: energy similarity (+0.47)
5. Pulse Overdrive by Kilowatt — Score: 0.45
   Because: energy similarity (+0.45)
```

No crash, but confirms `target_energy` isn't validated/clamped to a 0–1 range.

**4. Negative energy (-0.3)** — `{"genre": "pop", "mood": "happy", "energy": -0.3}`

```
1. Sunrise City by Neon Echo — Score: 3.00
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.00)
2. Gym Hero by Max Pulse — Score: 2.00
   Because: genre match (+2.0), energy similarity (+0.00)
3. Rooftop Lights by Indigo Parade — Score: 1.00
   Because: mood match (+1.0), energy similarity (+0.00)
4. Moonlit Sonata Study by Elara Quartet — Score: 0.45
   Because: energy similarity (+0.45)
5. Spacewalk Thoughts by Orbit Bloom — Score: 0.42
   Because: energy similarity (+0.42)
```

Energy term collapses to +0.00 for every song since `abs(energy - (-0.3))` always exceeds 1 — genre/mood alone dictate ranking. Confirms no input validation on `target_energy`.

**5. Acoustic-only freebie** — `{"genre": "polka", "mood": "ecstatic", "energy": None, "likes_acoustic": True}`

```
1. Midnight Coding by LoRoom — Score: 0.50
   Because: acoustic bonus (+0.5)
2. Library Rain by Paper Lanterns — Score: 0.50
   Because: acoustic bonus (+0.5)
3. Spacewalk Thoughts by Orbit Bloom — Score: 0.50
   Because: acoustic bonus (+0.5)
4. Coffee Shop Stories by Slow Stereo — Score: 0.50
   Because: acoustic bonus (+0.5)
5. Focus Flow by LoRoom — Score: 0.50
   Because: acoustic bonus (+0.5)
```

Five songs matching neither genre nor mood still tie at 0.50, purely from the acoustic bonus — a low-magnitude but real exploit of a single preference.

**6. All-None profile** — `{"genre": None, "mood": None, "energy": None, "likes_acoustic": False}`

```
1. Sunrise City by Neon Echo — Score: 0.00
   Because: no matching criteria
2. Midnight Coding by LoRoom — Score: 0.00
   Because: no matching criteria
3. Storm Runner by Voltline — Score: 0.00
   Because: no matching criteria
4. Library Rain by Paper Lanterns — Score: 0.00
   Because: no matching criteria
5. Gym Hero by Max Pulse — Score: 0.00
   Because: no matching criteria
```

Degrades gracefully to score 0.0 for everything; ties broken by stable-sort (CSV insertion order) since no explicit tie-breaker exists.

**7. Case/whitespace mismatch** — `{"genre": "Pop", "mood": "Happy", "energy": 0.82}`

```
1. Sunrise City by Neon Echo — Score: 1.00
   Because: energy similarity (+1.00)
2. Concrete Dreams by Vertex Flow — Score: 0.98
   Because: energy similarity (+0.98)
3. Rooftop Lights by Indigo Parade — Score: 0.94
   Because: energy similarity (+0.94)
4. Night Drive Loop by Neon Echo — Score: 0.93
   Because: energy similarity (+0.93)
5. Storm Runner by Voltline — Score: 0.91
   Because: energy similarity (+0.91)
```

**Bug found:** `"Pop"`/`"Happy"` matched nothing against the CSV's lowercase `"pop"`/`"happy"`, even though song 1 is a perfect fit. It only ranked #1 by energy luck, silently losing 3.0 points of genre/mood credit the user clearly intended. `score_song` should lowercase/normalize both sides before comparing.

**8. Tie-flood (lofi/chill/0.4)** — `{"genre": "lofi", "mood": "chill", "energy": 0.4}`

```
1. Midnight Coding by LoRoom — Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)
2. Library Rain by Paper Lanterns — Score: 3.95
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.95)
3. Focus Flow by LoRoom — Score: 3.00
   Because: genre match (+2.0), energy similarity (+1.00)
4. Spacewalk Thoughts by Orbit Bloom — Score: 1.88
   Because: mood match (+1.0), energy similarity (+0.88)
5. Coffee Shop Stories by Slow Stereo — Score: 0.97
   Because: energy similarity (+0.97)
```

No actual ties occurred in this dataset — energy proximity happened to differentiate all matching lofi/chill songs.

**Takeaway:** the most actionable fix is case-insensitive genre/mood comparison (found in profile 7); out-of-range energy values and the acoustic-only exploit are lower-severity design gaps worth documenting but not necessarily fixing for this assignment.

### Comparing profile pairs, in plain language

- **Profile 3 (energy 1.5) vs. Profile 4 (energy -0.3):** both "want" pop/happy songs, just with a broken energy number on opposite ends. Same top song both times (Sunrise City), but for different reasons — with 1.5, the energy score is small but not zero; with -0.3, it's flattened all the way to zero. This makes sense: an energy target that's too high still gets "closer" to real songs than one that's too low, since our songs top out at 0.97. The takeaway is the recommender doesn't know these numbers are invalid — it just does the math it's told to.

- **Profile 1 (rock/sad/high energy) vs. Profile 3 (pop/happy/too-high energy):** this is basically the "EDM profile prefers high energy, acoustic profile shifts to guitars" comparison. Profile 1 wants an intense rock song, and it gets one — "Storm Runner," a real rock song that also happens to be high energy. Profile 3 wants a happy pop song, and it gets "Sunrise City" — a real pop song that's also fairly high energy. Both results make sense on their face: each profile matched its genre, and the genre it matched happened to also be a decently high-energy song in this catalog. That's a coincidence of this dataset (the "happy" and "intense" songs both lean energetic), not something the code is smart enough to know on purpose.

- **Profile 5 (acoustic-only, nothing else matches) vs. Profile 8 (lofi/chill, energy 0.4 — a real match):** Profile 8 gets three well-reasoned lofi songs that actually fit chill mood and quiet energy — this is the system working as intended. Profile 5, by contrast, gets five random songs that share nothing with the user except "yes, these happen to be acoustic" — no genre, no mood, no energy connection at all. The comment: when a profile only turns on one dial (acoustic), the recommender can't tell the difference between "this song fits your vibe" and "this song just happens to also be recorded with acoustic instruments." It looks like a real recommendation, but it isn't one.

**Why does "Gym Hero" keep showing up for people who just want Happy Pop?**

Imagine you tell the system "I like pop music, and I'm feeling happy." The system doesn't actually know what "happy" sounds like — it just checks the "mood" label written on each song's file. "Sunrise City" is literally labeled genre=pop, mood=happy, so it's the correct answer and does show up first. But "Gym Hero" is also labeled genre=pop — it's just labeled mood=intense, not happy. So it earns the same +2.0 "I'm pop!" points as Sunrise City, and it's also a very high-energy song (0.93), so if a user's energy number happens to land anywhere near "high," Gym Hero can rack up almost as many points as the "actually happy" song — even though anyone listening to it would probably say it feels like a workout song, not a happy song. It shows up so often because in this small catalog, pop only has 2 songs total, and the system rewards "pop" and "high energy" so heavily that its only competitor for the genre slot keeps sneaking into the top 5 on energy points alone.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

- Normalize genre/mood comparisons (lowercase + trim) so casing differences like "Pop" vs "pop" stop silently losing points.
- Add tempo, valence, and danceability as optional scoring inputs, so users can express taste beyond genre/mood/energy/acoustic.
- Inject some controlled randomness or "explore" picks so the same profile doesn't always return an identical top 5.

---

## 9. Personal Reflection  

I have learned how recommender systems score and rank songs. I never realised how different a machine/model views things differently than humans. Everything for systems like this are all logical with no emotions. Somthing interesting that I discovered was how bias data can be an how bad/bias data can be very bad for systems. This project really changed my view about how models are structured because everything is seems so complicated for just recommending songs.
