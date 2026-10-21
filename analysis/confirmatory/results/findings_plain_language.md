# What the numbers say, in plain language

*A second page of results, written for a reader trained in medical anthropology and social science rather than statistics. The full tables, confidence intervals and sensitivity checks are in [results.md](results.md). Every number here comes from that file; nothing is rounded past the first decimal in the tables and nothing is softened.*

## The question we asked

When people say they feel confident handling health information, does that confidence follow their actual reading ability? No public survey asks the same American adults both things, so the study puts two national surveys side by side.

- **HINTS 7 (2024)** asked about 7,000 U.S. adults how confident they are filling out medical forms by themselves. We count the share who answered "very confident."
- **PIAAC Cycle 2 (2023)** gave about 3,800 U.S. adults a reading assessment and placed each person on a literacy scale. We count the share scoring at **Level 2 or above**, the level usually treated as adequate for everyday documents such as a medication label or an insurance letter. Adults at or below Level 1 are the group most of the literature calls "limited literacy."

Both groups were narrowed to adults aged 20 to 65 and sorted into the same three education groups: no high school diploma, high school diploma through associate degree, and bachelor's degree or higher. Then, group by group, we compare the confident share with the skilled share. The study design, the hypotheses and the exact numbers that would count as support were registered on OSF before the analysis ran, so none of what follows was chosen after seeing the data.

## Finding 1: reading skill climbs steeply with schooling; confidence climbs about half as fast

| Education | Very confident with medical forms | Reads at Level 2 or above |
|---|---|---|
| No high school diploma | 46% | 28% |
| High school through associate | 63% | 70% |
| Bachelor's or higher | 76% | 89% |

From the least to the most schooled group, measured reading skill rises **61 points**. Self-reported confidence rises **30 points**. The confidence ladder is about half as steep as the skill ladder. Both of the registered hypotheses asked for exactly this pattern, and both are supported with room to spare.

## Finding 2: among adults without a diploma, confidence outruns measured skill

In the no-diploma group, 46% say they are very confident, but 28% read at Level 2 or above. Confidence exceeds skill by **18 points**. In the two more-schooled groups the relationship flips: more people read at Level 2 or above than call themselves very confident (63% versus 70%, and 76% versus 89%).

So this is not a story of "everyone overestimates." The mismatch is specific to the group with the least schooling. One reading, offered as interpretation rather than a tested claim: the form question asks about a familiar everyday task, and people who manage without strong decoding skills have usually built ways to get through it, such as asking family or a clinic receptionist. Their answer reports coping. The assessment reports decoding. Both are real, and they diverge most where formal schooling is thinnest.

## Finding 3: the under-confidence of the better readers is a young-adult pattern

These breakdowns were planned as exploratory, so they are leads rather than findings.

- **Age 20 to 34:** 56% very confident, 76% at Level 2 or above. Young adults read well and say they are not very confident. The gap is 20 points.
- **Age 35 to 49 and 50 to 65:** confidence and skill match within a point or two.
- **Men** show a larger skill-over-confidence gap than women (9 points versus 3).
- **Self-rated health** makes little difference: the gap is about 6 to 7 points in both the good-health and fair-or-poor-health groups.

## Where Medicaid fits

Neither survey identifies Medicaid enrollees, which is why the registered analysis runs on education. To get a first look, we described the adult Medicaid population by education, age and sex from the 2024 American Community Survey and reweighted both surveys to match it. On that basis, adults who look like Medicaid enrollees are **60% very confident and 64% at Level 2 or above**. Privately insured adults are 67% and 76%. Uninsured adults are 57% and 63%.

Two cautions. This was a pilot run before registration, and it is disclosed as such. And the Medicaid literacy figure is a floor: matching on demographics cannot capture the other disadvantages that come with Medicaid enrollment, so the real skill share is probably lower and the real gap larger. The proper Medicaid comparison needs restricted data, which is the next phase.

## What this does and does not say

- It compares populations, not people. No one was both surveyed and tested.
- "Very confident" and "Level 2" are not the same yardstick. The registered comparison is about how each one changes with education, and where self-report and measurement part ways. That is what the design can answer.
- It does not say confidence is worthless or that people with limited literacy are fooling themselves. It says a confidence question and a reading assessment identify different people, and that the difference is largest among adults without a diploma.
- Every figure has a margin of uncertainty, because each comes from a sample. The no-diploma group is the smallest (232 people in HINTS, 311 in PIAAC), so its margin is the widest: the 18-point gap could plausibly be anywhere from 5 to 31 points. Even the low end is a real excess of confidence over skill. For the two larger groups the margins are narrow, and for the headline comparison across education the margin never comes close to zero.
- Eight pre-specified variations of the analysis (a stricter skill threshold, a looser confidence threshold, a different confidence question, a narrower age range, paper versus web respondents, and a different placement of some associate degrees) all reach the same conclusions.

## Why it matters

The single question about confidence with medical forms is one of the most widely used quick screens for health literacy. These results say it behaves differently depending on schooling. Among adults without a diploma it flags fewer people than a reading assessment would. Among adults with more schooling it flags more people than the assessment would. A screening or outreach approach that leans on self-report alone will therefore miss the most where need is greatest, and over-count where it is least. For a tool like HeaLSS, that argues for pairing self-report with a direct measure wherever the population's schooling is lowest, which is exactly where Medicaid enrollees are concentrated.
