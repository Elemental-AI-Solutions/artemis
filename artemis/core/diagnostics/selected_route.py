# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Secret-free static preflight descriptors, not task route or capability proof."""

from typing import Any

_PROVIDERS = frozenset(
    {"google", "vertexai", "openai", "anthropic", "openrouter", "xai", "ollama", "vllm", "custom"}
)
_SOURCE_KINDS = frozenset({"artemis_jsonc", "artemis_json", "llm_config_json", "other", "unknown"})
_ENDPOINT_KINDS = frozenset(
    {
        "sdk_default_unverified",
        "settings_base_override_present",
        "environment_base_value_present",
        "factory_local_default",
        "factory_api_default",
        "adc_managed_unverified",
        "unknown",
    }
)
_UNKNOWN_REASONS = frozenset(
    {"preflight_not_available", "invalid_preflight", "config_unavailable", "fake_model_mode"}
)


def _descriptor(
    state: str,
    reason: str,
    *,
    provider: str = "unknown",
    source_kind: str = "unknown",
    endpoint_kind: str = "unknown",
) -> dict[str, Any]:
    return {
        "version": 1,
        "label": "configured operator primary (static preflight)",
        "scope": "current_process_default_config",
        "role": "operator",
        "state": state,
        "reason": reason,
        "provider": provider,
        "source_kind": source_kind,
        "endpoint_kind": endpoint_kind,
        "verdict_policy": "legacy_credential_inventory",
        "snapshot": "readiness_snapshot_may_be_cached",
        "unverified": [
            "runtime_overrides",
            "effective_task_route",
            "task_environment_parity",
            "authentication",
            "endpoint_availability",
            "inference",
            "image_interpretation",
            "tool_calling",
        ],
    }


def unknown_configured_operator(reason: str = "preflight_not_available") -> dict[str, Any]:
    """Describe missing evidence without selecting a provider from inventory."""
    return _descriptor("unknown", reason if reason in _UNKNOWN_REASONS else "invalid_preflight")


def configured_operator_primary(
    provider: str,
    source_kind: str,
    *,
    settings_base_present: bool = False,
    environment_base_present: bool = False,
    fake_model: bool = False,
) -> dict[str, Any]:
    """Describe injected primary configuration using only fixed public categories.

    The caller supplies the parsed operator provider, not inventory order. Base
    flags describe settings/environment presence, not URL or credential validity;
    environment presence includes empty values. No fallback, profile or client
    is resolved.
    """
    if fake_model:
        return unknown_configured_operator("fake_model_mode")
    source = source_kind if source_kind in _SOURCE_KINDS else "other"
    if provider not in _PROVIDERS:
        return _descriptor("unsupported", "provider_unsupported", source_kind=source)

    if provider == "openai" and settings_base_present:
        endpoint_kind = "settings_base_override_present"
    elif provider in {"custom", "ollama", "vllm"}:
        endpoint_kind = (
            "environment_base_value_present"
            if environment_base_present
            else "factory_local_default"
        )
    elif provider in {"openrouter", "xai"}:
        endpoint_kind = "factory_api_default"
    elif provider == "vertexai":
        endpoint_kind = "adc_managed_unverified"
    else:
        endpoint_kind = "sdk_default_unverified"
    return _descriptor(
        "resolved",
        "static_config_only",
        provider=provider,
        source_kind=source,
        endpoint_kind=endpoint_kind,
    )


def render_configured_operator(value: Any) -> dict[str, Any]:
    """Rebuild an allowlisted descriptor; never echo arbitrary probe metadata."""
    if value is None:
        return unknown_configured_operator()
    if (
        not isinstance(value, dict)
        or type(value.get("version")) is not int
        or value["version"] != 1
    ):
        return unknown_configured_operator("invalid_preflight")
    if value.get("scope") != "current_process_default_config" or value.get("role") != "operator":
        return unknown_configured_operator("invalid_preflight")
    state = value.get("state")
    reason = value.get("reason")
    provider = value.get("provider")
    source = value.get("source_kind")
    endpoint = value.get("endpoint_kind")
    if not all(isinstance(item, str) for item in (state, reason, provider, source, endpoint)):
        return unknown_configured_operator("invalid_preflight")
    if source not in _SOURCE_KINDS or endpoint not in _ENDPOINT_KINDS:
        return unknown_configured_operator("invalid_preflight")
    if state == "unknown" and reason in _UNKNOWN_REASONS:
        return unknown_configured_operator(reason)
    if state == "unsupported" and reason == "provider_unsupported" and provider == "unknown":
        return _descriptor(state, reason, source_kind=source)
    if (
        state == "resolved"
        and reason == "static_config_only"
        and provider in _PROVIDERS
        and source != "unknown"
        and endpoint != "unknown"
    ):
        return _descriptor(
            state, reason, provider=provider, source_kind=source, endpoint_kind=endpoint
        )
    return unknown_configured_operator("invalid_preflight")
