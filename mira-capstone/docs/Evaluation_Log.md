# Evaluation Log - Evaluate, Fix, Re-evaluate

Use one entry per fix. The course rewards even one documented loop. This file is a template. Replace the text in `[brackets]` after you run the tests.

## Trace review checklist

- [ ] A trace exists for every test run
- [ ] I opened one vague input trace (T09 to T12) and checked whether any agent invented information
- [ ] I opened one detailed input trace (T05) and checked the output against the Prepare Context node
- [ ] I compared token cost for vague versus detailed inputs
- [ ] I calculated total cost per run

## Fix 1

| Field | Entry |
|---|---|
| Test ID | [for example T10] |
| Input | [text sent] |
| Agent that failed | [for example Status Reporter] |
| What went wrong | [for example it described Phoenix tasks that do not exist] |
| Evidence | [trace link or screenshot name] |
| Prompt change | [exact rule added, for example: "If the user names a project other than ABCDE Ltd., answer NOT AVAILABLE IN THE DATA."] |
| Output before | [paste] |
| Output after | [paste] |
| Result | [Fixed / Partly fixed / Not fixed] |
| Side effects checked | [re-ran T01 to T12, no new failures] |

## Fix 2 (optional)

[Same table.]

## Cost observation

| Input type | Tokens in | Tokens out | Cost (from Langfuse) |
|---|---|---|---|
| Detailed (T05) | [ ] | [ ] | [ ] |
| Vague (T09) | [ ] | [ ] | [ ] |

## Optional: fine-tuning record

| Item | Entry |
|---|---|
| Agent chosen | [for example Intent Classifier] |
| Training examples | [15: 10 clear, 5 vague with UNCLEAR] |
| Accuracy before | [ ] |
| Accuracy after | [ ] |
