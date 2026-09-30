# LOCALAI development setup — 2026-09-30

## Status

Godot **4.7.2** is installed; an isolated Windows export and its headless runtime both passed with exit code **0**. Portable .NET SDK **8.0.425** and current-user LM Studio **0.4.25+1** are installed and their version/CLI checks passed. Unity Hub is installed, but the pinned Editor installation failed at Windows elevation; Android modules are **not verified installed**. The Epic Launcher installer is downloaded and verified, but neither Launcher nor Unreal Engine is installed by this session. **ARTEMIS image/tool inference and Android app exploration remain unverified.**

This report records the LOCALAI host, not the separate workstation model-registration experiment in [the inference recovery checkpoint](artemis-inference-recovery-2026-09-30.md).

## Authorization and boundaries

The user authorized using LOCALAI for local AI/inference and development, installing necessary software there, installing Godot and Unity, and installing/using Unreal if feasible. This supersedes the earlier no-download/no-engine-install restriction **for LOCALAI installation work**, not the earlier workstation's limited registration window.

No paid purchase, account linking/settings change, unknown/shared process termination, firewall/shared-service change, persistent ARTEMIS provider/configuration change, heavy project build, or mobile task is inferred from that authorization. No credential values are included here. Saved RDP credentials were reused without extracting their values. Credential discovery followed BWS → BW → Vault PKI → documented host fallbacks.

Planning used the available pinned GPT-6-Sol subagent and installer research used GPT-6-Luna. A GPT-6.1-Sol route was not verified; the lead session was not switched to that model. Agent recommendations and peer reservation reports are not user approval.

## Direct host observations

An owned RDP connection to `localai.elementalai.local` authenticated to LOCALAI. Direct inventory found Windows 11 Pro, build 26200, x64, with a non-elevated user token. Historical Linux/VM notes were not used as current host inventory.

| Resource | Point-in-time observation |
| --- | --- |
| Host RAM | 31.93 GiB total; 19.06 GiB free |
| GPU | NVIDIA GeForce RTX 5060 Ti |
| VRAM | 16,311 MiB total; 8,792 MiB free |
| NVIDIA driver | 610.88 |
| C: | 139.9 GiB total; 82.8 GiB free |
| D: | 500.0 GiB total; 356.9 GiB free, before installations |
| WinGet | 1.29.380 |

These snapshots do not reserve capacity or prove that a vision model can allocate successfully. New engine/SDK files were placed on D: where possible to preserve C: headroom.

An existing `llama-server`, PID 6424, listens on `127.0.0.1:57459`. A read-only `/v1/models` response identifies `Qwen2.5-7B-Instruct-Q4_K_M`. This worker was not stopped, restarted, reconfigured, or sent a completion request. Its owner was not established. No listener on the configured ARTEMIS port 1234 was found in the selected-port inventory.

The existing LOCALAI Hugging Face snapshot `86835bf9949e4d14d6860f7910b1340ad4f271a9` under `D:/unsloth/huggingface/hub/models--unsloth--Qwen3.5-4B-MTP-GGUF/snapshots/` contains:

- `Qwen3.5-4B-UD-Q4_K_XL.gguf`: 2,990,664,000 bytes.
- `Qwen3.5-4B-UD-Q8_K_XL.gguf`: 6,065,971,520 bytes.
- `mmproj-F16.gguf`: 672,423,488 bytes.

Names/sizes and snapshot identity are inventory evidence, not a LOCALAI integrity check, successful projector load, image interpretation, or parsed tool-call proof. No model download or loading was performed in this checkpoint.

## LM Studio — installed; model/server not activated

WinGet package `ElementLabs.LMStudio` **0.4.25+1** installed with `--scope user --silent`. WinGet verified its installer hash and reported `Successfully installed`, exit code **0**.

- Official installer: <https://installers.lmstudio.ai/win32/x64/0.4.25-1/LM-Studio-0.4.25-1-x64.exe>.
- Saved installer: `D:/Engines/Installers/LM-Studio-0.4.25-1-x64.exe`.
- Actual SHA-256 matches catalog: `76c025ef4abf38edac36da09ce1a54d2803b3871a074b95bd9dffdb231458f0c`.
- Authenticode: **Valid**, signer **Element Labs Inc.**
- Installed application: `C:/Users/localuser/AppData/Local/Programs/LM Studio/LM Studio.exe`.

The application launched to its **0.4.25** first-run onboarding screen. The `Get Started`/terms continuation was not clicked; no account settings were changed. The CLI was absent immediately after installation and present after first launch at `C:/Users/localuser/.lmstudio/bin/lms.exe`; it reports commit **69d945a**. Startup output showed a CUDA runtime survey/preferences update. A subsequent `lms runtime ls` separately confirmed the selected installed engine `llama.cpp-win-x86_64-nvidia-cuda12-avx2@2.48.0`; other listed CPU/CUDA/Vulkan engines were version 2.41.0. This is LOCALAI runtime inventory, not the workstation's earlier 2.47.0 backend or inference proof.

Read-only CLI checks:

- `lms ls --llm --json`: `[]`.
- `lms ps --json`: `[]`, including the final recheck.
- `lms server status`: **The server is not running.**
- `lms import --help` confirms `--hard-link` and `--dry-run`; server/runtime help was inspected without invoking start, stop, update, remove, or load.
- An import **dry run only** for the existing D: Q4 candidate previewed `C:/Users/localuser/.lmstudio/models/unsloth/Qwen3.5-4B-MTP-GGUF/Qwen3.5-4B-UD-Q4_K_XL.gguf`. It explicitly reported no import was performed. Because the source is on D: and the default destination is on C:, that preview is not a workable same-volume hard-link registration or proof of a successful import. The final check found the source present and the previewed destination absent.

No model was registered, downloaded, loaded, or sent a completion request on LOCALAI. No LM Studio server was started, no listener was rebound, and no firewall/shared-service setting was changed. The pre-existing `llama-server` PID 6424 remained on `127.0.0.1:57459`; it was not adopted as an ARTEMIS route.

### Post-install capacity checkpoint

At `2026-09-30T16:10:39-04:00`, LOCALAI reported 31.93 GiB total RAM, **19.82 GiB free**, and **8,763 MiB free** of 16,311 MiB VRAM. The immediately following disk check found **72.94 GiB free on C:** and **351.64 GiB free on D:**. The selected-port query still found only PID 6424 on port 57459, not a port 1234 listener. These are point-in-time observations, not a reservation, load clearance, or configuration-sensitive allocation estimate.

## Godot — installed and bounded smoke verified

- Standard Windows x64 editor: **4.7.2.stable.official.ed1daf0bf**.
- Location: `D:/Engines/Godot/4.7.2-stable/`.
- Official release API: <https://api.github.com/repos/godotengine/godot-builds/releases/tags/4.7.2-stable>.
- Editor archive: `Godot_v4.7.2-stable_win64.exe.zip`.
- Editor SHA-256, verified against the release API asset digest and downloaded file: `731980f9608d61333e5baf54a2ef17210acc7a538446c0cb9969f002aca1e953`.
- `--headless --version` passed.
- An isolated minimal `smoke-project/project.godot` opened with `--headless --editor --path ... --quit`; exit code **0**.

Export templates `Godot_v4.7.2-stable_export_templates.tpz` were downloaded from the same official release, verified, and extracted to `D:/Engines/Godot/4.7.2-stable/export-templates/templates/`.

Template SHA-256: `f298490b8d44d934be425a5a65a51bf15f422428b229a06a6e11d9ffea248011`.

The current user's default destination `C:/Users/localuser/AppData/Roaming/Godot/export_templates/4.7.2.stable` was verified absent before creating a junction to the D: template directory. Reading `version.txt` through that junction returned `4.7.2.stable`. Windows, Android, Linux, macOS, iOS, and Web template files were listed. No existing template directory was overwritten.

The standard rather than .NET edition was selected because no Godot C# requirement or project pin was verified. An isolated scene and GDScript under the newly created `smoke-project/` print `ARTEMIS_GODOT_EXPORT_OK` and quit. The Windows debug export produced `build/smoke.exe` (103,176,704 bytes), `smoke.console.exe` (188,928 bytes), and `smoke.pck` (1,804 bytes).

Final verification used the `WindowsSmoke` preset: export timeout 60 seconds, runtime timeout 20 seconds, with cleanup restricted to the newly started smoke processes if they exceeded those bounds. Neither timeout was reached. **Export exit: 0. Exported headless runtime exit: 0.** The runtime printed the expected marker; final redirected export and runtime stderr files were empty. This verifies a small Windows template/export/runtime path, not a full project build, graphical rendering, or Android/iOS toolchain.

The first attempt failed at `main.tscn:1`, `Expected '['`. Byte inspection found `EF-BB-BF` before the scene's `[`; PowerShell's UTF-8 writer had added a BOM. Only the owned fixture was rewritten as BOM-less UTF-8. A subsequent run exported successfully but logged missing `include_filter`/`exclude_filter` keys; those keys were added, with `build/*` excluded. A redirected recheck then failed because `Windows Smoke` was split into separate process arguments; renaming the owned preset `WindowsSmoke` corrected that invocation. Only the final clean export and explicit runtime exit checks are counted as passing.

## .NET 8 — portable SDK installed

- SDK: **8.0.425**, Windows x64.
- Location: `D:/SDKs/dotnet/8.0.425/`.
- Official metadata: <https://raw.githubusercontent.com/dotnet/core/main/release-notes/8.0/8.0.31/release.json>.
- Archive: <https://builds.dotnet.microsoft.com/dotnet/Sdk/8.0.425/dotnet-sdk-8.0.425-win-x64.zip>.
- SHA-512, verified against official metadata and downloaded file: `f0b6f15bf6f1a0507205c0cb102ab99e1dee875c4682c8ed94665be1d580186a06b21455e83b3a01a0ff7f4cd887b67420f2e2fe09ed985534a4cea488ae1af9`.
- `dotnet.exe --list-sdks` returned `8.0.425 [D:\SDKs\dotnet\8.0.425\sdk]`, exit code **0**.

This is a portable installation, not a machine-wide SDK/PATH update. Call the executable explicitly or configure only an owned process's PATH/DOTNET_ROOT. Dirtstorm standalone tests were reported to require .NET 8; no Dirtstorm tests or build were run here.

An initial metadata query used the wrong JSON level and stopped with `Official archive metadata absent` before downloading/installing. The corrected query used `release.sdks[0].files`; only the subsequently verified installation is counted.

## Unity — Hub installed; Editor blocked

Unity Hub **3.22.0.65535** was installed successfully via WinGet package `Unity.UnityHub`; installer hash verification passed and the install returned exit code **0**.

- MSIX SHA-256: `e69ca81a99fa03410645684dccfe5046559a19c24bf40c3787de4f59a6fb4048`.
- Package: `UnityTechnologies.UnityHub_3.22.0.65535_x64__2vrhnee42bhxm`.
- Executable: `C:/Program Files/WindowsApps/UnityTechnologies.UnityHub_3.22.0.65535_x64__2vrhnee42bhxm/app/Unity Hub.exe`.

Redirected Hub CLI help was inspected and supports `install-path`, `editors`, `install`, and `install-modules`, including Android child modules. The installed-editor query returned `[]`. The prior install path `C:/Program Files/Unity/Hub/Editor` was inspected before changing it to the new D: location; readback confirmed `D:/Engines/Unity/Editors`.

Pinned installation requested:

- Unity **6000.3.19f1**, changeset **7689f4515d75**.
- Android Build Support with child modules (`--module android --childModules`): OpenJDK, Android NDK, CMake, SDK build/platform/command-line tools and platforms.
- Initial Windows Mono support comes with the Editor; Windows IL2CPP/Visual Studio Build Tools were not added without a verified project requirement.

The owned Hub installation process started at `2026-09-30T15:17:11-04:00`. Its captured output later reported:

> [Unity (6000.3.19f1)] failed to install. Error given: The Windows elevation prompt was cancelled or timed out.
>
> Failed to install.

Android support/NDK download percentages and queued child modules are **not** installation proof. No Editor version/revision check, module verification, license activation, login, project import, batch smoke, or build succeeded here. No admin credentials, UAC bypass, or protected policy edit was attempted.

Unity documents an administrator-configured standard-user installation policy; that is a separate administrator task, not a workaround authorized by generic installation permission. Reference: <https://docs.unity.com/en-us/engine/6000.6/manual/get-started/install-and-upgrade/ent-deployment/ent-unpriv-install>.

## Unreal — verified installer only

The WinGet catalog entry `EpicGames.EpicGamesLauncher` reports Launcher package version **1.3.210.0**, using `EpicInstaller-20.3.3.msi` from Epic's official download host. The MSI was downloaded to `D:/Engines/Installers/EpicInstaller-20.3.3.msi`.

- Actual SHA-256 matches catalog: `d55d79710edfeaa107a62f2ea007bec1eeeac8b715a43c2ba3858eec7bc60337`.
- Authenticode status: **Valid**.
- Signer: **Epic Games Inc.**

The installer was not executed in this checkpoint. Account entitlement, an engine version/project pin, installation elevation, MSVC/Windows SDK readiness, and engine/cache/intermediate disk budget remain unverified. No account linking, purchase, license/account settings change, source build, or Unreal project import was performed.

References: <https://store.epicgames.com/download> and <https://dev.epicgames.com/documentation/unreal-engine/install-unreal-engine>.

## ARTEMIS status and closure

A fresh `mobile_diagnose(device_serial='emulator-5554', verify_credentials=true)` still reported the custom endpoint timeout. The public OpenAI 401 used the existing local filler key and is not evidence of a custom-route authentication failure. Canonical runtime remains the root checkout, not this worktree. No persistent ARTEMIS configuration/environment changes were made.

Diagnosis and its safe self-heal recheck found `emulator-5554` absent, no active/queued ARTEMIS tasks, and only the out-of-scope physical Samsung attached. No self-heal changes were applied. Missing `scrcpy` is optional at this checkpoint. No physical-device action or emulator launch was performed.

The renewed **16:42–17:05 EDT** recheck is recorded in [the inference recovery audit](artemis-inference-recovery-2026-09-30.md#renewed-route-recheck--2026-09-30-16421705-edt). DNS resolved LOCALAI, but TCP 1234 timed out through the FQDN, LAN IPv4, and direct IPv6; LAN IPv4 RDP transport remained reachable. The owned RDP client's initial and post-restoration captures were black, and native capture failed. No remote input was sent during that recheck; host interaction paused. The worker, LM Studio inventory, source files, and capacity measurements above remain **earlier observations**, not newly refreshed host state. The exact cause of the endpoint/capture failures is not established, and no listener, firewall, model, or shared-service change followed.

The original task cannot close as **inference restored** until a scoped candidate consumes a synthetic image and produces a usable parsed tool call through ARTEMIS's actual adapter, the running MCP's effective route is separately verified after any authorized configuration/reload, and a successful app-exploration trace is obtained on `LLMStatus_API36_x86_64` / `emulator-5554`.

Development setup also remains partial: Godot editor/version, isolated Windows export/runtime, portable SDK inventory, and LM Studio application/CLI/runtime inventory checks passed. Unity Editor and Unreal build readiness are not established. No llmstatus Kotlin/test change or Android PR merge is included. Operational scratch, downloaded installers/models, credentials, and canonical pre-existing edits are excluded from the repository commit.

Remaining prerequisites:

1. Prepare a supported administrator installation path/window for the pinned Unity Editor and matching Android modules. Do not bypass UAC or change the protected standard-user installation policy. Editor version/revision, modules, licensing, and a bounded batch smoke still need verification.
2. Resolve Epic installation elevation/account entitlement, a justified Unreal version, Windows build tools, and disk budget before claiming Unreal ready. A signed MSI is not an installed engine.
3. For LOCALAI inference, first coordinate actual service/GPU ownership. One peer's report of no LOCALAI reservation does not clear other owners or the existing worker. Use a same-volume, source-preserving D: registration path if the existing vision bundle is adopted; the C: hard-link dry run was not executed. Verify integrity/runtime compatibility and current capacity before a bounded owned load.
4. Separately verify a no-device synthetic-image plus parsed-tool-call probe through ARTEMIS's adapter. Any owned server setup, FQDN reachability, persistent ARTEMIS route/environment change, and MCP reload/effective-route verification remain distinct steps; no shared bind/firewall change is authorized implicitly.
5. Re-establish only the designated emulator's ownership/readiness and obtain a successful ARTEMIS app-exploration trace. The attached physical Samsung remains out of scope.

This checkpoint may close as **partial LOCALAI tooling provisioned and documented**, but not as **ARTEMIS inference restored**, **Unity/Unreal build host ready**, or **Android testing unblocked**.
