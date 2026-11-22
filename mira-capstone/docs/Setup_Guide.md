# Setup Guide - Import and Connect Mira in n8n

Time needed: about 20 minutes.

> **Compatibility.** The workflow uses n8n 1.x LangChain nodes: Chat Trigger (v1.1), Basic LLM Chain (v1.5), OpenAI Chat Model (v1.2), Switch (v3.2), HTTP Request (v4.2), Set (v3.4), Code (v2). If a node shows a warning after import, update n8n to the latest version.

## 1. Publish the data to GitHub

1. Create a **public** repository named `mira-capstone`.
2. Upload everything in this folder (keep the `data/` folder name).
3. Confirm this URL opens in your browser (replace the placeholders):
   `https://raw.githubusercontent.com/<username>/mira-capstone/main/data/task_board.csv`

The workflow reads the four data files from this URL. A private repo will not work.

## 2. Import the workflow

1. In n8n, go to **Workflows > Add workflow > Import from file**.
2. Select `workflow/mira_n8n_workflow.json`.
3. You should see 33 items: 25 workflow nodes, 5 OpenAI model sub-nodes and 3 sticky notes.

## 3. Fix the connectors (checklist)

| # | Node | What to set | Required |
|---|---|---|---|
| 1 | **Config** | `baseUrl` = `https://raw.githubusercontent.com/<username>/mira-capstone/main` | Yes |
| 2 | **Config** | `asOfDate` = `2026-11-16` for the sample data (or `{{ $today.toFormat('yyyy-MM-dd') }}` for live data) | Yes |
| 3 | **OpenAI Model - Classifier** | Select your OpenAI credential | Yes |
| 4 | **OpenAI Model - Plan** | Select your OpenAI credential | Yes |
| 5 | **OpenAI Model - Risk** | Select your OpenAI credential | Yes |
| 6 | **OpenAI Model - Status** | Select your OpenAI credential | Yes |
| 7 | **OpenAI Model - Milestone** | Select your OpenAI credential | Yes |
| 8 | **Log to Langfuse** | Select the Langfuse Basic Auth credential (step 4 below) | Optional |
| 9 | **Config** | `langfuseHost` = `https://cloud.langfuse.com` (EU) or `https://us.cloud.langfuse.com` (US) | Optional |

### Create the OpenAI credential
1. n8n: **Credentials > Add credential > OpenAI API**.
2. Paste your API key and save. Name it `OpenAI account`.
3. Open each of the five OpenAI Model nodes and pick this credential.

You can change the model per node. Defaults: `gpt-4o-mini` for classifier, status and milestone; `gpt-4.1-mini` for plan and risk. If you change a model, also update the name in the **Build Trace** node (`agents` list) so Langfuse cost matches.

## 4. Connect observability (Langfuse)

1. Create a Langfuse project. Copy the **Public key** and **Secret key**.
2. In n8n: **Credentials > Add credential > Basic Auth**.
   - User = Langfuse **public** key
   - Password = Langfuse **secret** key
   - Name = `Langfuse API Keys`
3. Open **Log to Langfuse** and select this credential.
4. Run one chat message. In Langfuse you should see a trace named `mira-request` with tags `mira`, `capstone` and the intent, and one generation per LLM call. Langfuse calculates token usage and cost from the model name.

**Skip tracing for now:** right-click **Build Trace** and **Log to Langfuse**, then choose **Deactivate**. Disabled nodes pass data through, so the chat reply still works. A failed Langfuse call never blocks the reply (the node is set to continue on error).

**Using LangWatch instead:** replace the URL and body in **Log to Langfuse** with the LangWatch collector endpoint and payload described in the LangWatch docs. The **Build Trace** node already holds trace id, input, output, intent and model.

## 5. Test in the chat

1. Click **Open chat** (or **Test workflow**) and send:
   - `Generate this week's status report` - expect 31 tasks, Done 11, In Progress 3, Blocked 2, To Do 15.
   - `Which milestones are at risk?` - expect M5 and M6 RED.
   - `Help me with my project` - expect the clarification menu.
2. Check each node's output in the execution view. The **Prepare ... Context** node shows the exact facts the LLM received.

## 6. Activate and run the baseline tests

1. Toggle the workflow to **Active**. Keep Chat Trigger **Public** on.
2. Copy the Chat Trigger **Production URL**. The chat endpoint ends in `/chat`.
3. Run:
   ```
   python scripts/run_baseline_tests.py --url https://<your-n8n-host>/webhook/<webhook-id>/chat
   ```
4. Open `tests/test_results.md`. Review each output by hand and fill in the "Hallucination detected" row.
5. Take screenshots of: the workflow canvas, a chat run, and Langfuse traces. These are submission items.

## 7. Using your own data

Keep the file names and these column headers:

| File | Columns |
|---|---|
| `ABCDE_Ltd_project_description.txt` | free text |
| `timeline.csv` | milestone_id, milestone, phase, start_date, due_date, owner, depends_on |
| `task_board.csv` | task_id, task, milestone_id, owner, status, due_date, priority, notes |
| `risk_register.csv` | risk_id, risk, category, likelihood, impact, owner, mitigation, status |

Rules: dates are `YYYY-MM-DD`. Status is one of `To Do`, `In Progress`, `Blocked`, `Done`. Likelihood and impact are `High`, `Medium` or `Low`. `depends_on` lists milestone ids separated by `;`.

If your files have different column names or status words, edit the field names in the **Prepare Status Context**, **Prepare Milestone Context** and **Prepare Risk Context** Code nodes.

Different file names? Edit the file name in the matching **Fetch ...** HTTP Request node URL.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| HTTP node returns 404 | Repo is private, wrong branch, or wrong `baseUrl` | Open the raw URL in a browser. Make the repo public. Use `main` or your branch name. |
| "Credentials not found" on model node | Credential not selected after import | Select your OpenAI credential on that node. |
| Chat shows no reply | Chat Trigger response mode changed | In Chat Trigger > Options, set **Response Mode** to **When Last Node Finishes**. |
| Every request goes to the clarification menu | Classifier returned unexpected text | Open **Intent Classifier** output. Confirm it returns one word. Check the model credential. |
| Expression error in Code node | A Fetch node was renamed | Node names are referenced in code. Keep names unchanged, or update the `$('...')` calls. |
| Langfuse shows nothing | Wrong host or keys | Check region host and that the public key is the user. The reply still works. |
| Status counts look wrong | CSV status words differ | Statuses must match exactly: `To Do`, `In Progress`, `Blocked`, `Done`. |
