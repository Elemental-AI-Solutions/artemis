# ARTEMIS inference recovery checkpoint — 2026-09-30

## Status: registration complete; inference prerequisite not restored

The authorized local-only recovery phase registered an existing complete Qwen3.5-4B GGUF and matching vision projector using two hard links, then ran a resource estimate. **No model was loaded, no inference was run, and no application was explored.** Catalog capabilities and resource estimates do not satisfy the acceptance gate.

This is a documentation-only repository checkpoint. It does not implement the llmstatus Android accessibility retry correction, authorize a provider change, or clear mobile-test authoring or release acceptance.

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

Not performed: model loading, image/tool inference, ARTEMIS app exploration, Android build/instrumentation, mobile-test authoring, provider/configuration change, engine installation/update, paid inference, or PR merge.

This checkpoint can be closed as **local discovery/registration complete**, but the overall task cannot be closed as **ARTEMIS inference restored**. The Android exploration and retry-correction gates remain held. Only this report belongs in the recovery checkpoint commit; operational model files, credentials, and canonical pre-existing edits do not.
