# ARTEMIS credential-output hardening — 2026-10-01

## Status: bounded source-development checkpoint

This increment hardens **messages returned by `validate_api_key` and application-log messages generated within that validator**. It builds on local commit `6c317c3` and the [configured-operator preflight checkpoint](artemis-configured-operator-preflight-2026-10-01.md).

The validator no longer intentionally interpolates custom endpoint URLs, provider response bodies/reason phrases, arbitrary caller-supplied provider strings, or caught exception text into these outputs. It uses fixed labels/messages and integer HTTP status codes instead.

**This is not end-to-end log sanitization, restored inference, or a route-verdict correction.** HTTP transport logging, historical log output, and the unchanged MCP boundary remain separate exposure paths. Existing offline compatibility checks and static review do not constitute comprehensive leak-prevention proof.

## Implementation

Only [the credential validator](../../artemis/utils/credentials_validator.py) changes production behavior:

- Add `_http_failure_message` for fixed internal provider labels and HTTP status. A non-integer status produces a fixed status-unavailable message rather than formatting arbitrary content. Labels are assigned from literals in the existing dispatch branches, not reconstructed from caller input.
- For non-200 responses, stop calling or forwarding `_extract_error_message`. Response JSON, text, and reason phrases are not used to build validator-returned failure messages.
- Qualify HTTP 400 as `API key not valid or request rejected`. This preserves the existing Gemini compatibility substring without asserting that the key caused the rejection. It is a fixed diagnostic phrase, not provider-derived evidence or a capability result.
- Keep established fixed successful credential messages. Custom endpoint success becomes `Custom endpoint verified successfully.` without its URL; the no-base configuration result stays unchanged.
- Keep unknown-provider length-check behavior but return generic fixed text rather than the supplied provider name.
- Use a generic fixed label before branch selection/client construction, then branch-local fixed labels. Preserve the existing `is_google_family_provider` dispatch and alias predicates; add no alternative normalization or routing table.
- Remove exception payloads and raw provider names from timeout, network, and unexpected-error messages, both returned and logged. Warning/error levels remain unchanged. Add no traceback or exception-class serialization.
- Document the validator-owned output boundary and separate HTTP transport logging.

The `validate_api_key` signature, request URLs/methods/payloads/authentication headers, timeout, provider dispatch, empty/placeholder rules, status-based validity handling, custom `EMPTY` behavior, and unknown-provider length fallback remain unchanged by source inspection. The four-field MCP credential records and inventory-first blocked/degraded policy are not changed.

`_extract_error_message` remains unchanged for direct callers and its existing tests. It is still a **raw extraction helper**, not a public-text sanitizer. `_http_failure_message` likewise relies on fixed internal label callers; it is not a general arbitrary-label redactor.

## Review and delegation

- The existing Explore agent located output escape paths, caller propagation, logging sinks, reusable fixed-category conventions, and exact compatibility assertions. It did not modify source/tests or run live probes.
- The existing GPT-6-Luna-pinned agent supplied a context-only design assessment and independently reviewed the bounded production diff. It found no concrete issue in that diff; request/authentication, dispatch, timeout, and validity behavior appeared preserved. It did not run tests or probes.
- A read-only planning consultation was requested from the peer session named **Astra**, whose reported route is Claude Opus rather than a verified separate Astra model. Its delayed recommendations arrived after implementation commit `6df8988` and supported the bounded return/application-log checkpoint: fixed labels/statuses, qualified HTTP 400 wording, preserved raw helper contract and request/boolean/verdict behavior, and explicit transport/historical/MCP/route-policy deferrals. This was advice based on supplied context/excerpts, not independent source review or supervised orchestration. It did not authorize expanded scope. The suggested synthetic-canary coverage remains deferred under the standing ARTEMIS exploration gate; no new tests were authored.
- Orca did not recognize this ARTEMIS worktree. No repository registration, Run/Task/Dispatch, Orca worker, or supervised execution was established; native exploration/review is not represented as Orca supervision or a Ruflo swarm.

The lead integrated the change and ran the checks below. No peer advice was treated as authorization for runtime, model, service, device, or permission changes.

## Offline validation

Commands ran from the isolated ARTEMIS worktree with the existing canonical virtual-environment interpreter. No test code or ad-hoc executable assertion harness was authored. No provider requests, inference-capability probes, ARTEMIS device tasks, or new application exploration were performed.

Existing compatibility selection:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m pytest tests/unit/mcp/test_diagnose_tool.py tests/unit/test_credentials_validator.py -q -k 'not tool_signature_and_registration and not hung and not logs_surface and not attempt_fix'
```

Final result: **38 passed, 10 deselected in 0.81s**.

Lint:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m ruff check artemis/utils/credentials_validator.py
```

Result: **All checks passed!**

Formatting:

```bash
'D:/Github-EAI/artemis/.venv/Scripts/python.exe' -m ruff format --check artemis/utils/credentials_validator.py
```

The initial check reported one formatting-only correction in the HTTP 400 helper. It was fixed, then compatibility and source checks were rerun. Final result: **1 file already formatted**.

Whitespace:

```bash
git diff --check
```

Result: passed with no output, including staged validation of both task-owned files. Committed whitespace and clean-worktree checks are required before final closure.

**Coverage limitations:** the existing validator tests cover raw helper extraction, empty/placeholder handling, Gemini success/failure, and OCR success. MCP tests substitute `validate_api_key`, so passing them does not exercise production validator logging/message safety. There is no new targeted coverage for custom success, all HTTP categories, non-integer statuses, aliases/unknown-provider text, timeout/network/unexpected-error returns or logs, reflected/transformed/cross-target secrets, or transport/historical/MCP output. Ten cases were deselected and the broader suite was not run. New tests remain gated on successful ARTEMIS target-application exploration under the standing test-authoring instructions.

## Explicit residual exposure and deferred work

1. **Transport logs:** installed HTTPX 0.28.1 logs full request URLs at INFO in `_client.py`; HTTPCore emits DEBUG traces. Custom request URLs remain untouched. No global logger disabling/filter mutation, contextvar logging architecture, or third-party modification was introduced.
2. **Historical/raw logs:** MCP log-tail collection removes ANSI/truncates but does not sanitize arbitrary text. This increment neither reads nor cleans previously emitted logs, nor secures unrelated log producers.
3. **MCP boundary:** `_verify_credentials` still formats escaped exception text/arbitrary validator results and then performs literal replacement of the current target's exact key. Partial URLs, encoded/trimmed/cross-target credentials, substituted validator messages, and exceptions escaping outside the validator's caught region remain unbounded there. No MCP allowlist/schema change is included.
4. **Raw helper:** direct `_extract_error_message` callers still receive provider-controlled text. Public validation paths no longer invoke it, but retaining its contract is not general sanitization.
5. **Route policy:** credential inventory still determines diagnostic primary and verdicts. The public-OpenAI/custom-endpoint verification mismatch, exact target/auth/base association, anonymous-endpoint baseline, and summary/guidance reconciliation remain open. The static configured-operator descriptor does not repair them.

These residuals require separately scoped implementation and regression coverage. This checkpoint reduces validator-owned output exposure; it does not justify treating full diagnostic output or logs as secret-safe.

## Original recovery gates and operational boundary

Original acceptance still requires an authorized supplied synthetic image through ARTEMIS's real LLM adapter, image-dependent interpretation, and a usable parsed call to a bound harmless function schema. No returned function or device action may execute during the capability probe. Catalog discovery, credential presence, text-only completions, screenshots, and static descriptors remain insufficient.

Candidate/subprocess success is not proof of the running MCP's effective route. Applicable provider/model/paid-inference/routing/environment/shared-service changes require fresh authorization and preservation/rollback planning. Configuration/environment changes require MCP reload, followed by running effective-route verification and successful ARTEMIS target-app exploration on **`LLMStatus_API36_x86_64 / emulator-5554`**; no device substitution is authorized.

This implementation made no canonical `.env`, credential, runtime configuration, provider/model/server, installation, listener/process, device, MCP-reload, or Android changes. Orca was opened earlier for coordination discovery, but no ARTEMIS service or worker was launched through it. Nothing was pushed, published as a PR, merged, or placed under CI automation.

After the local commit and final clean-worktree verification, this session can close as a **credential-output-hardening development checkpoint**. Original inference recovery, route-verdict correction, broader log/MCP redaction, targeted security coverage, and Android acceptance remain incomplete.
