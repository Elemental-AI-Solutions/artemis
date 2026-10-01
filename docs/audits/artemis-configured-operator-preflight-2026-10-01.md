# ARTEMIS configured-operator preflight — 2026-10-01

## Status: static diagnostic development checkpoint complete

This increment adds a secret-free `configured_operator` field to `mobile_diagnose`. It describes the **configured operator primary (static preflight)** from the default configuration visible to the process producing the readiness snapshot. It does not attest a running task's effective route or establish authentication, endpoint availability, inference, image interpretation, or tool calling.

**Inventory-first credential verification and verdicts remain unchanged.** In particular, the public-OpenAI/custom-endpoint verification mismatch is not fixed. ARTEMIS inference recovery and successful target-application exploration remain incomplete.

The changes build on local commit `a199668` and the [previous recovery checkpoint](artemis-inference-recovery-2026-09-30.md). This report records source development and offline compatibility validation, not a new live recovery observation.

## Implementation

- [Configuration parser](../../artemis/config/llm.py): extract `parse_llm_config_with_source`, retaining filename precedence (`artemis.jsonc`, `artemis.json`, `LLM_CONFIG_FILENAME`), `get_config_path` behavior, JSONC parsing, default/node expansion, and Pydantic validation. Existing `parse_llm_config` callers still receive only `LLMConfig` and retain normal error logging. The diagnostic call disables parse-error logging.
- [Static descriptor](../../artemis/core/diagnostics/selected_route.py): accept injected categories/presence flags and build a versioned, fixed-category envelope. The helper logic has no environment reads, configuration/router/service imports, inference-client construction, network requests, or device actions. The existing parent-package import graph is not claimed to be side-effect-free.
- [Credential probe](../../artemis/core/diagnostics/probes/credentials_probe.py): quietly parse the default configuration and obtain the primary `operator` provider via `get_agent("operator")`. Add the envelope to the existing readiness metadata without changing credential inventory/order, statuses, actions, or blocker policy. Do not resolve profiles, fallbacks, or a live-verification target.
- [MCP output](../../mcp_server/tools/diagnose.py): rebuild the envelope through an allowlisted renderer, both at the top level and when scrubbing probe facts. Missing legacy metadata and timeout responses expose `unknown / preflight_not_available`; malformed envelopes expose `unknown / invalid_preflight`. Arbitrary extra metadata is not copied into the new field.

No new field contains raw credentials, URLs, model names, absolute paths, exception text, provider response bodies, or client objects. Configuration/preflight failures produce only `config_unavailable`; fake-model mode produces `fake_model_mode`. Neither case selects a provider from credential inventory.

## Evidence boundaries

The envelope is version 1, with scope `current_process_default_config` and role `operator`. Its `verdict_policy` is explicitly `legacy_credential_inventory`. It belongs only to the readiness snapshot, which may be cached; there is no global target cache or secret-bearing verification side channel.

- `resolved / static_config_only` means the default configuration was parsed and the operator provider was supported by the descriptor allowlist. It is not a readiness or capability verdict.
- `unsupported / provider_unsupported` exposes no raw unsupported provider value.
- `source_kind` identifies only a filename category: `artemis_jsonc`, `artemis_json`, `llm_config_json`, `other`, or `unknown`. It does not identify an absolute path, the directory-selection branch, or the runner's configuration ingress.
- Endpoint categories describe static inputs/defaults only. OpenAI consults Settings `OPENAI_BASE_URL`; custom/Ollama/vLLM consult environment `OPENAI_BASE_URL`, not the inventoried `OLLAMA_BASE_URL` or `VLLM_BASE_URL` variables.
- `environment_base_value_present` means the environment variable exists, including an empty or invalid value. It does not mean a valid override or reachable endpoint.
- SDK defaults and ADC-managed selection are explicitly unverified. The descriptor does not inspect downstream SDK behavior or discover ADC credentials.

The envelope explicitly leaves runtime overrides, effective task route, task-environment parity, authentication, endpoint availability, inference, image interpretation, and tool calling unverified. Named SDK profiles, standalone-runner overrides, daemon/task configuration, and executed fallbacks can differ from this default-file preflight.

## Review

The available GPT-6-Sol-pinned agent reviewed the staged design, and the GPT-6-Luna-pinned agent reviewed the bounded source changes. GPT-6.1-Sol routing was not verified; these were native subagent reviews, not Orca-supervised execution or a Ruflo swarm.

The independent code review found no other concrete blocker in the bounded increment. Its initial empty-environment fallback concern was withdrawn after checking the repository factory expression:

```python
base_url = endpoint.api_base or os.environ.get(
    "OPENAI_BASE_URL", "http://localhost:8000/v1"
)
```

`os.environ.get` uses that default only when the variable is absent; a present empty value is passed onward. The descriptor category was clarified from `environment_base_override_present` to `environment_base_value_present`, without changing selection semantics. Downstream SDK interpretation of an empty base was not inspected or exercised. The reviewer did not run tests or live probes.

Source/diff inspection found no changes to credential request dispatch, the four-field credential records, `_primary_credential`, baseline readiness, verdict calculation, summary, or REQUIRED/OPTIONAL credential guidance. This is static inspection, not new regression coverage.

## Offline validation

Commands ran from the isolated recovery worktree, using the existing canonical virtual-environment interpreter. No new test code or ad-hoc executable assertion harness was authored; no live inference or mobile-device task was run.

Existing compatibility selection:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m pytest tests/unit/mcp/test_diagnose_tool.py tests/unit/test_credentials_validator.py -q -k 'not tool_signature_and_registration and not hung and not logs_surface and not attempt_fix'
```

Final result after the category clarification: **38 passed, 10 deselected in 0.96s**.

Lint:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m ruff check artemis/config/llm.py artemis/core/diagnostics/probes/credentials_probe.py artemis/core/diagnostics/selected_route.py mcp_server/tools/diagnose.py
```

Result: **All checks passed!**

Formatting:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m ruff format --check artemis/config/llm.py artemis/core/diagnostics/probes/credentials_probe.py artemis/core/diagnostics/selected_route.py mcp_server/tools/diagnose.py
```

Result: **4 files already formatted**.

Whitespace:

```bash
git diff --check
```

Result: passed with no output, including staged validation of all five task-owned files before committing.

**Coverage limitation:** these existing tests use legacy mocked readiness metadata and verify compatibility with inventory-first behavior. They do not exercise real production of the new preflight, parser/source selection, descriptor categories, or malformed-envelope rendering. The ten deselected cases and the broader suite were not run. New targeted regression tests remain gated on successful ARTEMIS application exploration under the standing test-authoring instructions. Passing the compatibility selection does not prove the new preflight semantics.

## Deferred work and recovery gates

Still open:

1. Associate authorized authentication/base inputs with the actual live-verification target, rather than credential inventory.
2. Correct custom-endpoint verification and reconcile baseline credential policy, verdicts, summary, and REQUIRED/OPTIONAL guidance.
3. Harden legacy free-form credential/error URL redaction. Whole-string replacement does not establish safety for partial URLs, userinfo/query/path fragments, raw exceptions, provider response bodies, or HTTP logs. The new field's allowlist does not repair those existing surfaces.
4. Add targeted preflight/policy regression coverage after the required application exploration.

Original recovery acceptance still requires an authorized synthetic image through ARTEMIS's real LLM adapter with image-dependent interpretation, plus a usable parsed call to a bound harmless function schema. No returned function or device action may execute during that capability probe. Catalog flags, installed software, credential presence, text-only completions, screenshots, and static descriptors are insufficient.

Candidate/subprocess success must not be presented as proof of the running MCP's effective route. Applicable provider, model, paid-inference, routing/environment, or shared-service changes require fresh authorization, preservation/rollback planning, and MCP reload after configuration/environment changes. Verify the running effective route afterward, then obtain successful ARTEMIS application exploration on the designated `LLMStatus_API36_x86_64 / emulator-5554`; no substitute device is authorized.

## Operational boundary and closure

This increment made no canonical `.env`, credential, runtime configuration, provider/model/server, installation, listener/process, device, MCP-reload, or Android changes. It did not push, open a pull request, merge, or enable CI automation. Task-owned source and this report are intended for a local commit only.

This task/session can close as a **static-preflight development checkpoint** after the local commit and final clean-worktree verification. It must not close or relabel the original ARTEMIS recovery, route-verdict correction, or Android acceptance work as complete.
