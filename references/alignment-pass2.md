# Alignment pass 2

[Family guide](skill-family.md) · [Branding and handoffs](../BRANDING.md) · [Contributing](../CONTRIBUTING.md)

This pass reconciles the unfinished first rollout and extends the common package contract without changing specialist runtime behavior. Shared files now include the validator, regression suite, contributor guide, AGENTS.md, BRANDING.md, .editorconfig, PR template and package CI. The package CI runs on Linux, Windows and macOS with Python 3.12. Existing Quality workflows remain separate.

The validator requires base config.ini for config generators, checks all declared entry points/example inputs, validates the four local onboarding/contribution/branding/agent guides, rejects encoded traversal and unsupported URL schemes, and checks bounded PNG chunks/CRCs. Image decoding, visual review and factual approval remain outside its scope.

The library audit compares shared UTF-8 text after normalizing platform line endings, not arbitrary whitespace. Missing files, catalog/name mismatches, workspace escapes and real content drift fail. An error in one checkout is reported without skipping the remaining members.

## Windows installation plan

```powershell
python scripts/skill_library.py plan --shell powershell --destination ./skills
```

This prints literal-quoted commands without installing anything. POSIX remains the default. Both plans follow default branches rather than a pinned release. Private certificate inclusion is explicit and does not grant access.

## Verification

```bash
python -m unittest discover -s tests -p 'test_package_*.py' -v
python scripts/validate_package.py
python scripts/skill_library.py audit --workspace ./skills
```

The common tests group invalid metadata, required files, paths/links, symlinks, corrupt logos, activation names, base config and non-execution into parameterized cases. The hub also retains catalog/plan/audit tests and adds PowerShell, control-character, name-coherence and shared-file regressions.

Do not infer merge or registry-release status from this document. Verify each PR result and the exact tested head. Ledger onboarding must follow the actual ledger.py init/run CLI, not a fabricated manifest-preflight or test-runner interface.
