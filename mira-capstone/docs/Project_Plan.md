# Mira - Capstone Project Plan

## 1. Goal

Deliver a working multi-agent project assistant (Mira) in n8n, tested on a 12-case baseline dataset, traced in Langfuse, and documented for submission.

**Definition of done:** all items in the submission checklist (section 6) are complete and the GitHub repository is public.

## 2. Scope

| In scope | Out of scope |
|---|---|
| Plan, risk, status and milestone capabilities | Live Trello connection (optional extension) |
| Router pattern with a clarification fallback | Hierarchical multi-intent requests |
| CSV and text file inputs | Authentication, multi-user access |
| Langfuse tracing, cost analysis, 3 production metrics | Fine-tuning (optional, see section 7) |

## 3. Work plan (15 working days)

Steps follow the Capstone Playbook. Adjust the day numbers to your deadline.

| Phase | Playbook step | Days | Key tasks | Output |
|---|---|---|---|---|
| 1. Understand | Step 1 | 1 | Read the Mira problem statement. Write the 3-sentence problem summary. Hand-write one example output per capability. | Problem summary |
| 2. Select tools | Step 2 | 1 | Choose platform, LLMs, data access, observability. Record the reason for each. | Tool selection table |
| 3. Design | Step 3 | 2 | List tasks. Pick the router pattern and justify it. Define each agent with its guardrail. Draw the diagram. | Architecture diagram, agent specs |
| 4. Build | Step 4 | 5 | Day 1: Status lane only. Day 2: Plan lane. Day 3: Risk lane. Day 4: Milestone lane. Day 5: classifier, router, clarification menu. Test each lane alone before connecting. | Working workflow JSON |
| 5. Baseline test | Step 5 | 1 | Run 12 tests with `scripts/run_baseline_tests.py`. Review outputs by hand. | `tests/test_results.md` |
| 6. Evaluate and fix | Step 6 | 2 | Connect Langfuse. Read traces. Fix at least one failure in a prompt. Re-run the same test. Record before and after. | `docs/Evaluation_Log.md`, trace screenshots |
| 7. Document | Step 7 | 2 | Write the architecture writeup, cost analysis and metrics. Build the slide deck. Push to GitHub. | Writeup, deck, repo |
| Buffer | - | 1 | Rehearse the presentation. Fix last issues. | - |

## 4. Milestones

| ID | Milestone | Day | Exit check |
|---|---|---|---|
| P1 | Problem and tools agreed | 2 | Summary and tool table written |
| P2 | Design signed off | 4 | Diagram drawn, each agent has a guardrail rule |
| P3 | Status lane works end to end | 5 | T05 passes with exact counts |
| P4 | All four lanes plus router work | 9 | Tests T01 to T09 produce sensible output |
| P5 | Baseline suite documented | 10 | 12 tests recorded |
| P6 | One fix verified in traces | 12 | Before and after outputs saved |
| P7 | Submission package complete | 14 | Checklist ticked |

## 5. Deliverables

| Deliverable | File | Status in this repo |
|---|---|---|
| Workflow JSON | `workflow/mira_n8n_workflow.json` | Ready to import |
| Agent prompts | `prompts/*.txt` | Ready |
| Sample data | `data/*` | Ready (replace with official files if provided) |
| Baseline test dataset | `tests/baseline_test_dataset.csv` | Ready |
| Test runner | `scripts/run_baseline_tests.py` | Ready |
| Architecture diagram | `diagrams/mira_architecture.*` | Ready |
| Architecture writeup | `docs/Architecture_Writeup.md` | Draft ready. Add your test observations. |
| Evaluation log | `docs/Evaluation_Log.md` | Template. Fill in after your runs. |
| Slide deck | `presentation/Mira_Capstone_Presentation.pptx` | Ready. Add screenshots and test results. |
| Screenshots | `screenshots/` | You add: canvas, chat run, Langfuse traces |
| Test results | `tests/test_results.md` | Generated when you run the script |

## 6. Submission checklist

- [ ] Workflow JSON and README in a public GitHub repository
- [ ] Architecture diagram included
- [ ] Baseline test results documented for all 12 inputs
- [ ] Screenshots: workflow canvas, system in action, Langfuse traces
- [ ] Architecture writeup (1-2 pages) with all required sections
- [ ] All assignment questions (Q1 to Q4) answered
- [ ] Slide deck
- [ ] GitHub link submitted

## 7. Optional extensions

| Extension | Effort | Value |
|---|---|---|
| Trello live board (replace the task board CSV fetch with the Trello node) | Medium | Shows a real integration |
| Fine-tune the classifier on 15 examples (10 clear, 5 vague with UNCLEAR) | Medium | Recognised in scoring |
| Hierarchical "prepare my weekly review" (status + risks + milestones in one answer) | Medium | Handles multi-intent requests |

## 8. Project risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Official ABCDE data differs from sample columns | Medium | Medium | Edit field names in the three Prepare Code nodes (Setup Guide, section 7) |
| LLM invents content on vague input | Medium | High | Guardrail rules in every prompt, UNCLEAR route, run edge tests T09 to T12 |
| Classifier mislabels edge cases (T10, T11, T12) | Medium | Medium | Review traces, tighten classifier rules, re-run |
| n8n node version differences after import | Low | Medium | Update n8n. Re-add the affected node. |
| Observability set up too late | Medium | High | Connect Langfuse in phase 4, not phase 6 |
| API cost overrun | Low | Low | Small models, about USD 0.003 per request at most |
