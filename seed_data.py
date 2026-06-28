"""
Run this script once before the demo:
    python seed_data.py

This loads 3 weeks of Arjun's journal into Cognee so the demo
starts with a rich, connected memory graph.
"""

import asyncio
from memory_engine import store_entry

SEED_ENTRIES = [
    {
        "date": "2025-06-01",
        "text": "First placement drive tomorrow. I've been preparing for months but suddenly everything feels blank. What if I freeze during the technical round? My hands were literally shaking when I did a mock interview today. I need to sleep but my brain won't stop."
    },
    {
        "date": "2025-06-03",
        "text": "Didn't get through the first round at Infosys. It's fine. Everyone says the first one doesn't matter. But I keep replaying the moment they said 'we'll let you know' and I knew it was over. Ate alone in the mess today. Didn't feel like talking to anyone."
    },
    {
        "date": "2025-06-05",
        "text": "Called home today. Dad asked about placements first thing. Mom was quieter than usual. I didn't tell them about the rejection. I said 'still waiting.' I hate that I lied but I couldn't bear the silence that would follow. Dad has already told relatives I'll get placed at a good company."
    },
    {
        "date": "2025-06-07",
        "text": "Rishi got placed at TCS today. He treated everyone to dinner. I was happy for him, genuinely. But walking back to the hostel I felt this heaviness. Like I'm falling behind on a timeline I never agreed to. Why does everyone seem to know what they're doing except me?"
    },
    {
        "date": "2025-06-09",
        "text": "Couldn't focus on DSA practice today. Sat in front of my laptop for 3 hours and did nothing. Watched YouTube. Felt guilty. Watched more YouTube. The loop is real. I know what I should do but I just... can't start."
    },
    {
        "date": "2025-06-11",
        "text": "Another drive today. Deloitte. Made it to round 2. First time I've gotten this far. The interviewer smiled a few times which I think is a good sign? Trying not to get my hopes up. But for the first time in a week I felt like maybe I'm not completely behind."
    },
    {
        "date": "2025-06-13",
        "text": "Didn't get Deloitte either. Round 2 cutoff. I know logically that hundreds of people apply. But logic doesn't help at 1am when you're staring at the rejection email. I haven't been sleeping well. I keep waking up at 3am with this tight feeling in my chest."
    },
    {
        "date": "2025-06-15",
        "text": "Mom called again. She mentioned my cousin got placed last month. I know she wasn't trying to compare but it stung. I love my family but lately every call feels like a progress report I'm failing. I wish I could just disappear for a month and come back with an offer letter."
    },
    {
        "date": "2025-06-17",
        "text": "Had a good conversation with my senior Priya today. She said she got rejected 11 times before her first offer. Something about that number — 11 — made me feel better. Like there's a path through this, it's just longer than I thought. Studied for 4 hours tonight. Felt like myself again."
    },
    {
        "date": "2025-06-19",
        "text": "The chest tightness is back. I think I'm burnt out. I've been grinding for placement prep for 4 months straight without a real break. My hobbies feel far away — I used to draw, used to play chess. Haven't touched either in months. Who am I outside of this placement season?"
    },
    {
        "date": "2025-06-21",
        "text": "Applied for 3 more companies this week. I'm going through the motions now. Resume, apply, prepare, interview, wait, reject, repeat. I wonder if I even want these jobs or if I just want to stop feeling like a failure. That's probably not the right reason to want a job."
    },
    {
        "date": "2025-06-23",
        "text": "Terrible sleep again. Dreams about interviews. In the dream the interviewer keeps asking questions I don't understand and I can't speak. Classic anxiety dream I guess. Told Rishi about it and he laughed but kindly. He said he had the same dreams before his interview. Maybe I'm not the only one."
    },
    {
        "date": "2025-06-25",
        "text": "Something small happened today. A junior asked me to help them with sorting algorithms. I explained it and they got it immediately. That felt good. Really good. I forgot that I actually know things. The placement process makes you feel like you know nothing. But I do know things."
    },
    {
        "date": "2025-06-27",
        "text": "Why have I been feeling so off lately? I can't put my finger on it. It's not one thing. It's like a low hum of unease that doesn't go away. Even on okay days there's this background noise. I don't know how to make it stop."
    }
]


async def seed():
    print("Seeding MemoryMirror with Arjun's journal entries...")
    print("This will take a minute — Cognee is building the memory graph.\n")

    for i, entry in enumerate(SEED_ENTRIES, 1):
        print(f"[{i}/{len(SEED_ENTRIES)}] Storing entry from {entry['date']}...")
        try:
            await store_entry(entry['text'], entry['date'])
            print(f"  ✓ Stored and connected.")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("\n✅ Seed complete. MemoryMirror is ready with 3 weeks of Arjun's memories.")
    print("Run the app with: streamlit run app.py")


if __name__ == "__main__":
    asyncio.run(seed())
