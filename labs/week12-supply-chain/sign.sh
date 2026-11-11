#!/usr/bin/env bash
# Sandbox/teaching only; for authorized lab use.
#
# Week 12 — SBOM generation + keyless signing/verification (Sigstore/Cosign).
# Demonstrates OWASP 2025 A08 Software or Data Integrity Failures defenses:
#   1) Push the image to a registry (cosign cannot sign a bare local image —
#      the signature is stored as a sibling artifact IN the registry).
#   2) Produce a CycloneDX SBOM from the image (component inventory).
#   3) Sign the pushed image keylessly (OIDC) with cosign.
#   4) Verify the signature — and show that an unsigned image FAILS.
#
# Keyless signing ties the signature to an OIDC identity (e.g. your GitHub
# or Google login) via Sigstore's Fulcio CA + Rekor transparency log, so
# there is no long-lived signing key stored by this demo. CWE-321 specifically
# refers to a hard-coded cryptographic key, not every managed long-lived key.
#
# All steps run in throwaway containers (--rm). Idempotent.
# NOTE: the push (step 1) and the SBOM/verify steps (2, 4) need no login and
# work offline against the throwaway local registry this script starts. ONLY
# the sign step (3) needs a browser/OIDC flow (your GitHub or Google login) —
# in class this is a guided demo one person drives, not something all 36 of
# you repeat individually. Everyone else can still run 1, 2 and 4, and run 4
# again afterwards against the now-signed image to see PASS.

set -e

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_IMAGE="${1:-week12-supplychain:lab}"

REGISTRY_NAME="week12-registry"
REGISTRY_PORT="${COSIGN_REGISTRY_PORT:-5500}"
IMAGE="localhost:${REGISTRY_PORT}/${LOCAL_IMAGE}"

cleanup() { docker rm -f "$REGISTRY_NAME" >/dev/null 2>&1 || true; }
trap cleanup EXIT

echo "==> [1/4] Start a throwaway local registry and push ${LOCAL_IMAGE} to it"
# cosign signs a REGISTRY reference, not a bare `docker images` tag — mounting
# the Docker socket lets trivy/cosign *read* the local image, but there is
# nowhere to attach a signature until the image lives in a registry. This
# local registry (no credentials, HTTP, throwaway) is enough for that; it is
# NOT where your real images belong (push there instead, with real auth).
cleanup
docker run -d --rm --name "$REGISTRY_NAME" -p "${REGISTRY_PORT}:5000" registry:2 >/dev/null
for i in $(seq 1 15); do
  curl -fs "http://localhost:${REGISTRY_PORT}/v2/" >/dev/null 2>&1 && break
  sleep 1
done
docker tag "$LOCAL_IMAGE" "$IMAGE"
docker push "$IMAGE"
echo "    Pushed $IMAGE"

echo
echo "==> [2/4] Generate CycloneDX SBOM with trivy"
# Expected output: sbom.cdx.json listing every component + version.
# Hand this to auditors / store it as a build artifact (SLSA provenance input).
docker run --rm -v "$HERE:/src" -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image \
  --format cyclonedx --output /src/sbom.cdx.json "$LOCAL_IMAGE"
echo "    Wrote $HERE/sbom.cdx.json"

echo
echo "==> [3/4] Keyless sign the PUSHED image with cosign (OIDC flow — guided demo)"
# COSIGN_EXPERIMENTAL=1 enables keyless mode on older cosign builds.
# --network host so the cosign container can reach localhost:$REGISTRY_PORT.
# This opens an OIDC login; the cert is logged to Rekor (public transparency).
docker run --rm -it -e COSIGN_EXPERIMENTAL=1 --network host \
  gcr.io/projectsigstore/cosign:latest sign --yes "$IMAGE"

echo
echo "==> [4/4] Verify the signature"
# Expected: PASS for the freshly-signed image. The '.*' below are DEMO
# WILDCARDS, not a pinned identity: they just mean "keyless, any OIDC
# identity/issuer" so this script works no matter who in class drove the
# sign step. A real gate pins BOTH to the specific signer you trust, e.g.
#   --certificate-identity 'https://github.com/<org>/<repo>/.github/workflows/release.yml@refs/heads/main'
#   --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
# so an attacker-signed image from a DIFFERENT identity is rejected — with
# '.*' here, any valid keyless signature from anyone passes.
# cosign is NOT installed on your host, so verification also runs in a
# container — don't try a bare `cosign verify` on your laptop, it isn't there.
docker run --rm -e COSIGN_EXPERIMENTAL=1 --network host \
  gcr.io/projectsigstore/cosign:latest verify \
  --certificate-identity-regexp '.*' \
  --certificate-oidc-issuer-regexp '.*' \
  "$IMAGE"

echo
echo "==> Negative test: verifying an UNSIGNED image must FAIL (this is good)."
echo "    Same container, no login needed — run it yourself:"
echo "    docker run --rm --network host gcr.io/projectsigstore/cosign:latest verify \\"
echo "        --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' python:3.9-slim"
echo "    # expect: Error: no signatures found   (both identity flags are required in keyless mode)"
