# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.



Some prompts to answer:

  In the design of my system, I have Categorical features and Numerical features. The Categorical features are used to award match bonuses for genre and mood, while the Numerical features (energy, tempo_bpm, valence, danceability, and acousticness) are used to score how close a song is to the user's target values. Every song is scored this way and then ranked highest to lowest. Each `UserProfile` stores what genre, mood, energy level, etc. that specific user typically likes, and every song is compared directly against that one profile's stated preferences. This is a **content-based filtering** approach — it recommends songs based on their own features matching what the user says they like, not based on what other similar users enjoyed.

  The system will skew toward "more of the same" — safe, genre-locked picks — and under-value songs that are good near-matches on mood/energy but sit outside the favorite genre.



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loading songs from data/songs.csv...
Loaded songs: 18

Top recommendations:

1. Sunrise City by Neon Echo — Score: 3.98
   Because: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

2. Gym Hero by Max Pulse — Score: 2.87
   Because: genre match (+2.0), energy similarity (+0.87)

3. Rooftop Lights by Indigo Parade — Score: 1.96
   Because: mood match (+1.0), energy similarity (+0.96)

4. Concrete Dreams by Vertex Flow — Score: 1.00
   Because: energy similarity (+1.00)

5. Night Drive Loop by Neon Echo — Score: 0.95
   Because: energy similarity (+0.95)
   
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



