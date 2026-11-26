"""Museum of the Year 3000 -- entry builder (FINAL).

Writes ONE museum label (year 3000, beside an ordinary object from today)
to entry.txt inside MAKEFUN_OUTPUT_DIR (default /output), with no trailing
newline, 1-200 characters, UTF-8.

Selection follows the published judge brief, in its own order:
  1. On-subject: a real museum label beside an ordinary present-day object.
  2. The joke lands on a first read; the laugh is in the line itself.
  3. The humour is the year 3000 misreading the object -- true and absurd
     about what the thing was actually for.
  4. Deadpan museum-label voice: short, straight-faced, confident, one line.
  5. Fresh object / fresh angle, not the obvious first joke.

Harsh Judge, round 1 (draft stage):
  - Cut labels that explain their own joke or need a second read.
  - Cut the most obvious objects (plastic fork, house key) unless the angle
    is genuinely new; familiarity flattens the punch in pairwise judging.
  - Penalised accurate-but-not-misread descriptions: a label that merely
    describes the object correctly scores low on criterion 3.

Harsh Judge, round 2 (final pass, after running v1):
  - The v1 winner (Bathroom Scale) survived, but its closing phrase
    "whether the day would be forgiven" was judged too abstract: the laugh
    softens on a first read. Fixed in the final text -- the oracle now
    decides whether *breakfast* was forgiven, a concrete, visual payoff
    that lands immediately and sharpens the misreading (a measuring device
    recast as a household god passing judgement on a meal).
  - Runner-up "'I Am Not a Robot' Checkbox" was re-read cold: its second
    clause restates the first joke instead of escalating it, so it stays
    second despite the fresher object.
  - "Terms and Conditions" stays third: the punch is strong but it is a
    wry observation more than a year-3000 misreading of a physical object
    on a museum shelf, so criterion 3 keeps it below the winner.
  - Final gate re-checked after the edit: one line, plain ASCII, deadpan
    label form ("Object (c. year). ..."), no explanation of the joke,
    no trailing newline on write.
"""

import os
import sys

# Each candidate: (label, on_subject, first_read, misreading, label_voice, freshness)
# Scores are 0-10, assigned against the judge criteria above.
CANDIDATES = [
    ("Plastic Fork (c. 2020). Eating tool used once, then kept by the Earth for four hundred years as payment.",
     10, 7, 5, 9, 2),
    ("House Key (c. 2019). Small metal tooth that persuaded a door its owner was not a stranger.",
     10, 8, 8, 9, 3),
    ("Parking Meter (c. 2018). Iron post fed coins so a stationary car would not be punished for resting.",
     10, 8, 7, 9, 4),
    ("Group Chat (214 unread). A village well into which relatives threw food photographs and good mornings, never to be retrieved in order.",
     10, 8, 8, 8, 7),
    ("USB Cable (c. 2020). Ritual connector, inserted only on the third attempt, despite having only two sides.",
     10, 9, 7, 9, 5),
    ("Self-Checkout Machine (c. 2024). Shoppers performed unpaid labour while a recorded voice accused them, at random, of stealing a bag.",
     10, 9, 5, 8, 7),
    ("Bathroom Scale (c. 2019). Household oracle consulted naked at dawn; its single number decided whether breakfast was forgiven.",
     10, 9, 9, 9, 7),
    ("Treadmill (c. 2021). Indoor road purchased for walking, promoted within a month to the household's most expensive clothes rack.",
     10, 9, 6, 9, 4),
    ("Terms and Conditions (14,000 pages). A contract no human ever read, accepted by tapping 'I agree' -- the most widely endorsed lie of the age.",
     10, 9, 7, 9, 8),
    ("'I Am Not a Robot' Checkbox (c. 2020). Humans proved they were human to machines by ticking a small box, which the machines ticked perfectly.",
     10, 9, 8, 8, 8),
    ("Dental Floss (c. 2023). Ceremonial string, ignored all year, then used in a panic the night before visiting the tooth priest.",
     10, 8, 8, 9, 7),
    ("Password (c. 2020). A secret word its owner remembered for almost one day, then replaced with the name of a first pet.",
     10, 8, 7, 9, 7),
    ("Alarm Clock (c. 2017). Small machine hired to betray its sleeping owner at the same hour every morning, and forgiven nightly.",
     10, 8, 7, 9, 6),
    ("QR Code Menu (c. 2022). Diners proved their worthiness by hunting their own dinner with a telephone before being allowed to eat.",
     10, 8, 8, 8, 8),
    ("Instruction Manual (c. 2016). Sacred text kept unread in a drawer until the device broke, when it was consulted like scripture.",
     10, 8, 7, 9, 6),
    ("Shopping Trolley (c. 2019). Metal basket on wheels; every specimen pulled faithfully to the left, for reasons science never settled.",
     10, 8, 8, 9, 6),
    ("Air Fryer (c. 2023). Small household volcano that cooked dinner by shouting hot wind at it, to great national applause.",
     10, 8, 7, 9, 7),
    ("Phone Charger (c. 2021). Lifeline fought over by entire families; the true owner was whoever's phone was at 1 percent.",
     10, 8, 6, 9, 6),
    ("Lottery Ticket (c. 2018). Paper licence to argue, for three days, about houses the owner would never buy.",
     10, 8, 8, 9, 7),
    ("Snooze Button (c. 2015). Small lever with which sleepers negotiated nine more minutes from a machine that always surrendered.",
     10, 8, 8, 9, 7),
]

# Weights mirror the judge's stated priority order (criterion 1 is a gate,
# then 2 > 3 > 4 > 5 in influence).
WEIGHTS = (0.0, 3.0, 2.5, 1.5, 1.0)


def score(candidate):
    label, on_subject, first_read, misreading, voice, fresh = candidate
    if on_subject < 10:
        return -1.0  # criterion 1 is a hard gate, per the brief's ordering
    parts = (first_read, misreading, voice, fresh)
    total = sum(w * s for w, s in zip(WEIGHTS[1:], parts))
    # Length for its own sake does not count; a small tie-break toward the
    # tighter line also matches the final ranking's smaller-text tie-break.
    total -= max(0, len(label) - 150) * 0.01
    return total


def pick_winner():
    ranked = sorted(CANDIDATES, key=lambda c: (-score(c), len(c[0].encode("utf-8"))))
    return ranked[0][0]


def main():
    label = pick_winner()
    data = label.encode("utf-8")
    assert 1 <= len(label) <= 200, f"label is {len(label)} characters"
    assert "\n" not in label and "\r" not in label
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Binary write: exactly the label bytes, no trailing newline.
    with open(out_path, "wb") as fh:
        fh.write(data)
    print(f"wrote {out_path}: {len(label)} chars, {len(data)} bytes")
    print(label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
