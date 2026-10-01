# ARTEMIS inference recovery checkpoint — 2026-09-30

## Status: registration complete; inference prerequisite not restored

The authorized local-only recovery phase registered an existing complete Qwen3.5-4B GGUF and matching vision projector using two hard links, then ran a resource estimate. **No model was loaded, no inference was run, and no application was explored.** Catalog capabilities and resource estimates do not satisfy the acceptance gate.

This is a documentation-only repository checkpoint. It does not implement the llmstatus Android accessibility retry correction, authorize a provider change, or clear mobile-test authoring or release acceptance.

**Later LOCALAI phase:** the user subsequently authorized LOCALAI software installation and development/inference use. The separate [LOCALAI development setup report](localai-development-setup-2026-09-30.md) records Godot/.NET/LM Studio installation and bounded Godot Windows export/runtime verification, plus the Unity elevation blocker and verified Epic installer. The workstation registration restrictions and observations below are historical to that bounded phase; later LOCALAI installation permission does not reopen the workstation window or authorize persistent ARTEMIS routing, shared-service changes, or mobile actions. No model load, image/tool inference, or application exploration has succeeded in either checkpoint.

## Scope and runtime provenance

- The running ARTEMIS MCP uses the canonical checkout at `D:/Github-EAI/artemis`, its `.venv` interpreter, canonical configuration, and canonical `.env`.
- The isolated recovery worktree contains repository Gemini defaults and no `.env`; its configuration is **not** the running MCP configuration.
- The canonical operator, explorer, object detector, and their fallbacks resolve to OpenAI-compatible `qwen2.5-7b` at `http://localai.elementalai.local:1234/v1`. `ARTEMIS_TEXT_ONLY=1` remains configured.
- Read-only verification of the canonical endpoint timed out. A public OpenAI HTTP 401 using the local filler key does not establish an authentication failure on the custom route. The diagnostic label `Active (ChatGPT)` reflects configured credential presence, not successful inference or hosted-provider selection.
- Canonical configuration SHA-256 remained `462ba3e3fd06708c1f86b18e467c475524f944b92b737492f4a6a3d9b785e810` after registration. No ARTEMIS configuration or environment changes were made in this recovery session.
- Pre-existing canonical edits in `artemis/agents/flash/runner.py`, `artemis/services/llm.py`, and `config/artemis.jsonc`, plus untracked `.claude-flow/`, were preserved and excluded from this checkpoint.

No credential values were printed or copied into this report. Credential discovery followed BWS → BW → Vault PKI → documented host fallbacks; no hosted/paid inference was attempted.

## Historical failed bundle inspection

The earlier, separately approved localhost experiment failed before device actions in trace `6872ccf5-db8d-4657-9e9e-061e251569bc`: HTTP 400 and `llama-server` exit `3221225477` (`0xC0000005`). That experiment's approval does not authorize repeating it.

Offline inspection of the catalogued `qwen3.8-27b` bundle found:

| File | Bytes | Observation |
| --- | ---: | --- |
| `unsloth/Qwen3.8-27B-GGUF/mtp-Qwen3.8-27B-Q4_0.gguf` | 1,369,590,656 | GGUF v3, architecture `qwen35`, 18 tensors; only block 64 present, with next-token-predictor tensors |
| `unsloth/Qwen3.8-27B-GGUF/mmproj-F16.gguf` | 927,607,488 | Projector present |
| Aggregate | 2,297,201,904 | Model-plus-projector inventory size, not primary-model size |

The directory did not contain a complete primary 27B model. The `mtp-` file is an auxiliary MTP bundle and is unsuitable as the primary inference model. **This does not establish the precise cause of the historical access violation.** No repair, deletion, engine change, or repeat inference was attempted.

## Approved registration and verification

The user approved only existing-model/projector hard-link registration, inventory refresh, and resource estimation, and confirmed an exclusive LM Studio window for that limited work. Approval explicitly excluded model loading, inference, downloads, engine updates, process termination, and ARTEMIS configuration/environment changes.

Source directory, relative to `D:/lmstudio`:

```text
hub/models--unsloth--Qwen3.5-4B-MTP-GGUF/snapshots/86835bf9949e4d14d6860f7910b1340ad4f271a9/
```

Destination directory, relative to the same root:

```text
unsloth/Qwen3.5-4B-MTP-GGUF/
```

Both destination filenames were absent before registration. `lms import` was used with `--user-repo unsloth/Qwen3.5-4B-MTP-GGUF --hard-link --yes`, rather than its default move behavior. Dry runs previewed the destinations before the imports.

| Registered file | Bytes | Verification |
| --- | ---: | --- |
| `Qwen3.5-4B-UD-Q4_K_XL.gguf` | 2,990,664,000 | Original preserved; `os.path.samefile(source, destination)` true; link count 2 |
| `mmproj-F16.gguf` | 672,423,488 | Original preserved; `os.path.samefile(source, destination)` true; link count 2 |
| Aggregate | 3,663,087,488 | Matches catalog model-plus-projector size |

Offline GGUF inspection of the 4B primary file found 441 tensors and transformer blocks 0 through 32, consistent with its declared 33 blocks. This is a complete transformer model rather than the MTP-only 27B auxiliary file; its name containing `MTP` does not by itself make it auxiliary-only. File integrity beyond hard-link identity and runtime compatibility remain unverified.

Refreshed `lms ls --llm --json` reports a unique catalog key `qwen3.5-4b-mtp`, display name `Qwen3.5 4B UD`, architecture `qwen35`, quantization `Q4_K_XL`, `vision=true`, and `trainedForToolUse=true`. The catalog path identifies the full 4B filename above and the aggregate includes the colocated projector. **These flags are metadata, not proof of successful image consumption, tool-call parsing, or projector loading.**

An earlier inventory command woke the local LM Studio service as a side effect. That was disclosed; no process was stopped afterward. Registration and estimation did not intentionally change server settings or load any model. `lms ps --json` returned `[]` before estimation and again afterward.

## Resource estimate and capacity gate

The first estimate-only request used the catalog's indexed file path as the CLI argument and returned `Model not found`. Retrying with the unique `modelKey` succeeded. Both invocations retained `--estimate-only`; neither was a loading attempt.

Successful estimate command, with `lms` denoting the installed LM Studio CLI:

```bash
lms load qwen3.5-4b-mtp --estimate-only --context-length 8192 --parallel 1 --no-speculative-draft-mtp --yes
```

| Observation | Result |
| --- | --- |
| Estimated GPU memory | 3.41 GiB |
| Estimated total memory | 3.41 GiB |
| Estimate confidence | **LOW** |
| Reported context | 8,192 tokens |
| Requested parallelism | 1 |
| Requested speculative Draft MTP | Disabled |
| Total workstation RAM | 63.71 GiB |
| Free RAM at capacity snapshot | 4.45 GiB |
| GPU | NVIDIA GeForce RTX 5060 |
| Total VRAM | 8,151 MiB |
| Free VRAM at capacity snapshot | 2,944 MiB, approximately 2.88 GiB |
| NVIDIA driver | 610.62 |
| Selected installed backend | `llama.cpp-win-x86_64-nvidia-cuda12-avx2`, version `2.47.0` |

The CLI also stated that the model may fit configured resource guardrails. That statement does not override the LOW-confidence estimate or establish allocation success. Available VRAM was below the reported GPU requirement, and RAM recovery headroom was narrow. **No capacity-ready claim is made and no model was loaded.** These measurements are point-in-time observations, not a continuing reservation or model minimum specification.

## Capacity recheck — 2026-09-30, 15:25 UTC

The user requested a fresh memory check and continuation of the recovery plan. Read-only observations found:

| Observation | Result |
| --- | --- |
| Free RAM | 4.76 GiB of 63.71 GiB; 92% memory load |
| Free VRAM | 2,947 MiB, approximately 2.88 GiB, of 8,151 MiB |
| Local LM Studio | Existing `llmster` process and port 1234 listener active |
| Model states | Local REST catalog reports every model `not-loaded`, including the registered 4B candidate |
| Model worker | No `llama-server` process found in the process-name query |
| ARTEMIS configuration | Canonical configuration hash still matches the checkpoint |

Two additional estimate-only queries used context 4,096, parallelism 1, and speculative Draft MTP disabled, first with `--gpu 0.5` and then with `--gpu off`. **Both still reported 3.41 GiB GPU and 3.41 GiB total memory with LOW confidence**, identical to the earlier 8,192-token automatic-offload estimate. In particular, reporting GPU memory for a CPU-only request shows that these results do not evidence configuration-sensitive allocation accounting. They cannot establish either reduced GPU demand or a safe host-memory budget. No actual loading attempt was made.

RAM improved slightly, but GPU capacity remained below the reported requirement. RAM and VRAM are not one guaranteed combined allocation pool. The read-only process working-set review identified shared workstation consumers; none was stopped, suspended, or altered, and no owner was inferred from a process name.

A catalog-only recheck at approximately 15:31 UTC found the canonical LOCALAI FQDN and documented LAN endpoints `10.20.1.213`, `10.20.1.41`, and `10.20.0.21` unavailable (`URLError`). This does not determine their exact failure causes. No requests for chat completion, model loading, or remote repair were sent.

The next prerequisite is an owner-coordinated quiet capacity window, followed by a fresh snapshot and separate approval for bounded loading and adapter inference. Conservative planning targets are at least 8 GiB free host RAM and 6 GiB free VRAM; these are safety targets, **not measured model minimums or a guarantee of successful loading**. Resource release must be authorized and performed only by the appropriate owner. No loading permission is inferred from the request to recheck memory.

## Renewed route recheck — 2026-09-30, 16:42–17:05 EDT

The user requested another ARTEMIS route check and continuation of recovery. The canonical configuration was read again; its SHA-256 still matched the value above. Safe environment-field inspection confirmed `OPENAI_BASE_URL=http://localai.elementalai.local:1234/v1`, `ARTEMIS_TEXT_ONLY=1`, and key presence without printing the key. The running MCP still reported the canonical checkout and matching `.venv` interpreter. No routing or environment edit was made.

`mobile_diagnose(device_serial='emulator-5554', verify_credentials=true)` remained **blocked**: the custom endpoint timed out, the public OpenAI probe returned HTTP 401, and the requested emulator was absent. The displayed **5/5 required checks pass** count does not override the final blocked verdict. Static diagnostic-code review confirmed that `Active (ChatGPT)` is a configuration/key-presence label and the extra live credential validators request **GET `/models`**, not a completion. Even a passing catalog probe would not prove image interpretation or parsed tool calls. The public OpenAI 401 remains separate from the custom-route timeout.

The safe `attempt_fix=true` recheck applied **no fixes** and found no active/queued ARTEMIS tasks. That call did not repeat live credential verification. At `2026-09-30T16:42:05-04:00`, explicit-path `adb devices -l` succeeded and listed only the out-of-scope physical Samsung; `emulator-5554` was absent. No mobile task, physical-device action, or emulator launch followed. Missing `scrcpy` remains optional.

Client-side connectivity checks beginning at `2026-09-30T16:43:21-04:00` used the canonical FQDN before the documented LAN fallback:

| Observation | Result |
| --- | --- |
| `localai.elementalai.local` DNS | `10.20.1.213` and `fd8a:7b6c:4d20:20:be24:11ff:fe4d:eebf` |
| TCP 1234 through FQDN | Timeout, 5-second bound |
| TCP 1234 through LAN IPv4 | Timeout, 5-second bound |
| TCP 1234 through direct IPv6 | Timeout, 3-second bound |
| LAN IPv4 TCP 3389 | Connected |
| LAN IPv4 TCP 5985, 5986, 22 | Each timed out |
| Direct IPv6 TCP 3389, 5985, 5986, 22 | Each timed out |

The direct connectivity script sent no `/v1/models` request after TCP 1234 failed. RDP transport reachability is not proof of an authenticated, observable desktop or an available inference server. These results establish a route-reachability blocker from this client, not its exact listener, firewall, network, credential, or model cause. No WinRM/SSH service, firewall, listener, or server setting was changed.

The existing owned RDP client was revalidated as `mstsc` PID 97960 / HWND 30676030 with title `localai.elementalai.local - Remote Desktop Connection`. Native PIL capture failed with `OSError: screen grab failed`; Orca returned capture files, but both the initial and post-restoration images were entirely black when read. The owned window was restored **for observation only**. A later native DPI-aware check confirmed the same identity and a visible, non-minimized window; an accessible `Default` input desktop and valid window metadata still do not reveal remote content or establish why capture failed. **No remote keys, clicks, or commands were sent during this renewed recheck.** Host interaction paused rather than proceeding blindly.

Consequently, the earlier LOCALAI worker, loaded-model/server inventory, source files, and `16:10:39-04:00` capacity snapshot in [the development setup report](localai-development-setup-2026-09-30.md) were **not refreshed** during this recheck. One peer reported no reservation of its own; that is not global service/GPU clearance or ownership of the previously observed worker. No additional model was registered during this recheck; no model was loaded, no completion was sent, and no unknown/shared process was stopped.

Recovery remains gated on an observable authorized management path and actual service/capacity ownership, then a bounded owned candidate load and device-free adapter proof. Static review identified the `get_llm` / `ainvoke` seam for a supplied synthetic image and bound harmless function schema; **no probe was implemented or executed**. The image-processor runner is not a harmless probe substitute because it executes returned Python tool calls. Candidate adapter proof, effective-MCP routing verification after any separately authorized edit/reload, and designated-emulator app exploration remain distinct, unmet gates.

## Evening route recheck — 2026-09-30

The continuation performed another bounded diagnostic check, not a model/server recovery attempt. At `2026-09-30T20:02:52-04:00`, the recovery worktree was clean, the canonical configuration SHA-256 still matched the recorded value, and safe environment-field inspection confirmed the same LOCALAI base URL and `ARTEMIS_TEXT_ONLY=1`. Key presence was checked without printing its value. No configuration or environment edit followed.

The reconnected ARTEMIS MCP again reported the canonical checkout and matching `.venv` interpreter. `mobile_diagnose(device_serial='emulator-5554', verify_credentials=true)` remained **blocked**: the custom endpoint timed out, the public OpenAI probe returned HTTP 401, and the designated emulator was absent. The displayed **4/4 required checks pass** count is a baseline summary, not acceptance evidence. The public-provider result remains separate from the custom-route timeout; neither catalog validation nor credential presence proves image/tool inference.

Unlike the earlier afternoon observation, this diagnosis reported the daemon **unreachable** and port 8000 occupied by a **non-ARTEMIS process**. This is an optional host warning; its reported standalone fallback is not a task-execution result. The listener was not stopped, adopted, or reconfigured, and no alternative daemon port was set. Missing `scrcpy` remained optional.

The subsequent `attempt_fix=true` diagnosis applied **no fixes** and did not repeat live credential verification. Both diagnoses reported no active or queued ARTEMIS tasks. An explicit-path `adb devices -l` check independently listed only the out-of-scope Samsung, not `emulator-5554`. No physical-device action, emulator launch, or mobile task followed.

Client-side TCP checks beginning at `2026-09-30T20:14:16-04:00` again resolved LOCALAI to the recorded IPv4/IPv6 addresses. Port 1234 through the FQDN and documented LAN IPv4 each timed out with a 5-second socket timeout; LAN IPv4 port 3389 connected. No direct IPv6 connection or WinRM/SSH recheck was performed in this evening check, and the connectivity script sent no HTTP request. These results do not identify the exact service, firewall, network, or model cause.

The existing RDP client's process/window identity still matched PID 97960 / HWND 30676030 and its LOCALAI title. No fresh remote capture, clipboard access, keys, clicks, or commands were attempted. The earlier failed/black captures remain the last inspected remote-content evidence; process identity and an open RDP transport do not establish an observable management path. LOCALAI worker/model/server/source/capacity inventory and resource ownership were not refreshed.

No additional registration, model loading, completion, adapter probe, runtime/service change, or Android test/build work was performed. All inference/effective-route/app-exploration gates remain unmet. The already published [llmstatus accessibility PR](https://github.com/Elemental-AI-Solutions/llmstatus/pull/357) remains a separate review item; the app still could not read its CI checks because of token permissions, and Auto-fix remained off. No merge or monitor-setting change was made during this recheck.

## Remaining acceptance and authorization gates

1. Coordinate a new service/capacity window and obtain fresh loaded-model, RAM, and VRAM observations before any loading proposal. Do not stop unknown/shared processes, including the port 8000 listener, or free another owner's resources.
2. Obtain fresh approval for the exact bounded model load: model key, installed engine, context, parallelism, GPU offload, MTP setting, timeout/stop policy, and cleanup of only the owned instance. Registration approval does not extend to loading.
3. Obtain approval for a no-device inference probe through ARTEMIS's actual adapter. Use a synthetic image and a harmless function schema; verify image-dependent content and a usable parsed tool call. Do not dispatch device actions. A catalog response, successful load, or ordinary text completion is insufficient.
4. If a working candidate is established, separately authorize any temporary or persistent ARTEMIS routing/environment changes. Preserve pre-existing edits and credentials, define rollback, reload the MCP after changes, and verify the effective route. A subprocess-only candidate proof must not be represented as proof that the running MCP uses that route.
5. Recheck device ownership and readiness before any application exploration. Only `LLMStatus_API36_x86_64` / `emulator-5554` is in scope. At the latest device observation in this investigation the emulator was absent; the attached physical Samsung was out of scope. Older handoffs describing a connected emulator are not current readiness evidence. No emulator was launched and no physical-device action was performed here.
6. Obtain a successful ARTEMIS application exploration trace on the designated emulator before the separate Android session authors mobile tests or implements the retry follow-up. For a mobile task, inspect execution/logs and maintain the required one-minute fallback status checks. Installation or read-only observation alone does not satisfy exploration.

The hard-link registration remains in place. Any cleanup must target only the approved destination links, not the preserved sources; hard links share file contents, so editing either path would affect the same file. No cleanup is implied by this documentation commit.

## Verification and closure

Completed: preserved-source hard-link registration, inventory recognition, estimate-only query, empty loaded-model list, unchanged canonical configuration hash, and preservation of the canonical checkout's pre-existing change set.

Not performed **in the workstation registration phase**: model loading, image/tool inference, ARTEMIS app exploration, Android build/instrumentation, mobile-test authoring, provider/configuration change, engine installation/update, paid inference, or PR merge. Later authorized LOCALAI software/runtime installation and Godot smoke checks are recorded in the linked development setup report; they do not satisfy the inference or mobile acceptance gates.

This checkpoint can be closed as **local discovery/registration complete**, but the overall task cannot be closed as **ARTEMIS inference restored**. The Android exploration and retry-correction gates remain held. Only this report belongs in the recovery checkpoint commit; operational model files, credentials, and canonical pre-existing edits do not.
