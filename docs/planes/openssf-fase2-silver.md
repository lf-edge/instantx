# Plan — OpenSSF Best Practices Badge: Fase 2 «Silver»

> **Estado:** plan, **pendiente de implementación**. Documento de seguimiento de la Fase 2 (Silver), junto a [`openssf-fase1-passing.md`](./openssf-fase1-passing.md). Las acciones aquí descritas aún **no se han ejecutado**.

---

## 1. Contexto

InstantX (proyecto **12224** en bestpractices.dev) alcanzó **Passing (100%)** en la Fase 1. Esta fase busca el tramo **Silver** (criterios nivel 1), que mantiene todos los criterios Passing y añade ~30 más centrados en gobernanza, aseguramiento de calidad (CI, cobertura ≥80%), seguridad (threat model, validación de entrada, releases firmados) y documentación (roadmap, gobernanza).

**Estado de partida (verificado en `main`, jun 2026):**
- CI: **no existe** `.github/workflows/` (solo `.github/dependabot.yml`).
- Tests: solo `deployment/nifi/nifi-scripts/tests/test_encoder_decoder.py`; **EventPublisher y kafka_speed_exporter sin tests** → cobertura ~25-30%.
- Releases: tags `1.0.0`/`2.0.0` **sin firmar**; no hay proceso de firma.
- Gobernanza: `MAINTAINERS.md` (4 mantenedores Vodafone) pero sin `GOVERNANCE.md` ni roles/decisión documentados.
- Roadmap: sección en README es un **placeholder**.
- Seguridad: `SECURITY.md` cubre reporte + postura cripto; **sin threat model** ni proceso de respuesta detallado; validación de entrada mínima en `EventPublisher.py`.
- DCO: dependabot firma sus commits; **no exigido** a humanos.

## 2. Decisiones tomadas (preguntas bloqueantes — resueltas)

| # | Pregunta | Decisión |
|---|----------|----------|
| 1 | ¿Qué publica como "release"? | **Solo tags/código en GitHub** → `signed_releases` se cumple firmando los **tags de versión**. |
| 2 | Mecanismo de firma | **Sigstore keyless (`gitsign`)** para firmar tags/commits; sin gestión de claves GPG. |
| 3 | DCO/CLA | **DCO obligatorio + enforcement**: `Signed-off-by`, documentado en CONTRIBUTING y validado en CI. |
| 4 | Alcance | **Integral**: cubrir todos los criterios Silver, organizado en sub-fases ejecutables. |

## 3. Alcance

**Entra:** todos los criterios Silver (Basics, Change Control, Reporting, Quality, Security, Analysis); CI (tests+lint+SAST+DCO+cobertura), tests para EventPublisher y exporter hasta ≥80%, releases firmados con Sigstore, threat model/assurance case, validación de entrada, gobernanza/roles, roadmap real, y este doc de seguimiento.

**No entra:** criterios **Gold** (revisión por 2 personas obligatoria, ≥2 contribuidores de ≥2 organizaciones, cobertura 90%/branch 80%, etc.); cambios funcionales de producto no relacionados con los criterios.

---

## 4. Mapeo por criterio OpenSSF Silver (núcleo del plan)

Leyenda: **M** = MUST · **S** = SHOULD · **g** = SUGGESTED · *(ap)* = «si aplica».

### 4.1 BASICS

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `achieve_passing` | M | ✅ Met | Ninguna | — |
| `contribution_requirements` | M | ✅ Met | Ninguna (ya en CONTRIBUTING) | `CONTRIBUTING.md` |
| `dco` | S | ❌ | Exigir `Signed-off-by`; documentar + check en CI | `CONTRIBUTING.md`, `.github/workflows/ci.yml` |
| `governance` | M | ❌ | Crear `GOVERNANCE.md` (modelo de decisión, cómo se aceptan cambios, cómo ser mantenedor) | `GOVERNANCE.md` (nuevo) |
| `code_of_conduct` | M | ✅ Met | Ninguna | `CODE_OF_CONDUCT.md` |
| `roles_responsibilities` | M | ❌ | Documentar roles (mantenedor, revisor, responsable de seguridad/release) | `GOVERNANCE.md`, `MAINTAINERS.md` |
| `access_continuity` | M | ⚠️ | Documentar continuidad: ≥2 admins del repo, el proyecto sigue si alguien falta ≤1 semana | `GOVERNANCE.md` |
| `bus_factor` | S | ✅ Met | 4 mantenedores | `MAINTAINERS.md` |
| `documentation_roadmap` | M | ❌ | Roadmap real a ≥1 año (hitos/áreas) sustituyendo el placeholder | `ROADMAP.md` (nuevo) + enlace en README |
| `documentation_architecture` | M | ✅ Met | Ninguna (diagramas + docs) | `README.md`, `docs/` |
| `documentation_security` | M | ⚠️ | Documentar requisitos/expectativas de seguridad y supuestos del despliegue | `SECURITY.md` o `docs/Security-Architecture.md` |
| `documentation_quick_start` | M | ✅ Met | Ninguna | `deployment/Quick-Start.md` |
| `documentation_current` | M | ✅ Met | Mantener docs al día (auto-declaración) | — |
| `documentation_achievements` | M | ✅ Met | Badge OpenSSF ya enlazado en README | `README.md` |
| `accessibility_best_practices` | S | ⚠️ | Sin GUI (API/CLI); asegurar Markdown semántico/alt-text en imágenes del README; justificar | `README.md` |
| `internationalization` | S | ⚠️ | El software no localiza UI; justificar N/A razonado | — |
| `sites_password_security` | M *(ap)* | N/A | El código no almacena contraseñas | — |

### 4.2 CHANGE CONTROL

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `maintenance_or_update` | M | ⚠️ | Documentar ruta de actualización entre versiones (SemVer + notas de upgrade) | `RELEASE.md`, `CHANGELOG.md` |

### 4.3 REPORTING

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `report_tracker` | M | ✅ Met | GitHub Issues | — |
| `vulnerability_report_credit` | M | ❌ | Añadir política de crédito a quien reporta (salvo anonimato) | `SECURITY.md` |
| `vulnerability_response_process` | M | ⚠️ | Documentar proceso de respuesta (triaje → fix → disclosure coordinada + timeline) | `SECURITY.md` |

### 4.4 QUALITY

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `coding_standards` | M | ⚠️ | Nombrar la guía concreta (PEP 8, aplicada por ruff) | `CONTRIBUTING.md`, `docs/Development.md` |
| `coding_standards_enforced` | M | ❌ | Ejecutar ruff (y bandit) en CI como gate | `.github/workflows/ci.yml` |
| `automated_integration_testing` | M | ❌ | CI que corre la suite en cada push/PR de ≥1 rama | `.github/workflows/ci.yml` |
| `regression_tests_added50` | M | ⚠️ | Política: añadir test de regresión por bug; demostrar ≥50% en 6 meses | `CONTRIBUTING.md`, tests |
| `test_statement_coverage80` | M | ❌ | Añadir tests a EventPublisher y kafka_speed_exporter; gate cobertura ≥80% | tests nuevos + CI |
| `test_policy_mandated` | M | ✅ Met | Ninguna | `CONTRIBUTING.md` |
| `tests_documented_added` | M | ✅ Met | Ninguna | `CONTRIBUTING.md`, PR template |
| `warnings_strict` | M | ⚠️ | Tratar warnings como error en CI; valorar ampliar reglas ruff | `.github/workflows/ci.yml`, `pyproject.toml` |
| `external_dependencies` | M | ✅ Met | requirements.txt + pyproject | — |
| `dependency_monitoring` | M | ✅ Met | Dependabot | `.github/dependabot.yml` |
| `updateable_reused_components` | M | ✅ Met | deps fijadas + dependabot | — |
| `interfaces_current` | S | ✅ Met | Código modernizado (ruff UP) | — |
| `installation_common` | M | ⚠️ | Documentar install/uninstall (`docker-compose up`/`down`) | `deployment/Quick-Start.md` |
| `installation_development_quick` | M | ✅ Met | `poetry install` / docker-compose | `docs/Development.md` |
| `installation_standard_variables` | M *(ap)* | N/A | No es paquete del SO | — |
| `build_standard_variables` / `build_preserve_debug` / `build_non_recursive` | M/S *(ap)* | N/A | Python no compilado | — |
| `build_repeatable` | M *(ap)* | ⚠️ | Fijar **digests** de imágenes base en Dockerfiles; deps ya fijadas; documentar | `deployment/**/Dockerfile*` |

### 4.5 SECURITY

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `implement_secure_design` | M | ⚠️ | Documentar/aplicar principios (least privilege, validación, defaults seguros) | `docs/Security-Architecture.md`, `SECURITY.md` |
| `input_validation` | M | ❌ | Validación por allowlist en EventPublisher (sub_service/geohash/payload, límites de tamaño) | `deployment/eventPublisher/EventPublisher.py` |
| `hardening` | S | ⚠️ | Endurecer: límites de request, usuarios no-root (✅), digests de imagen, headers; documentar | Dockerfiles, `EventPublisher.py`, `docs/Security-Architecture.md` |
| `assurance_case` | M | ❌ | **Threat model + trust boundaries** + cómo el diseño los mitiga | `docs/Threat-Model.md` (nuevo) |
| `signed_releases` | M | ❌ | Firmar tags de versión con **Sigstore gitsign** + documentar verificación | proceso release, `RELEASE.md`/`docs/Development.md` |
| `version_tags_signed` | g | ❌ | Igual que arriba (tags firmados) | — |
| `crypto_credential_agility` | M *(ap)* | ✅/doc | Credenciales por env/`.env` (no hardcodeadas), actualizables sin recompilar | `docs/Security-Architecture.md` |
| `crypto_used_network` / `crypto_tls12` | S *(ap)* | ⚠️ | Documentar que brokers/HTTP soportan TLS 1.2+ | `docs/Security-Architecture.md` |
| `crypto_certificate_verification` | M *(ap)* | ⚠️/N/A | Documentar verificación de certificados TLS por defecto en clientes (o N/A) | `docs/Security-Architecture.md` |
| `crypto_weaknesses` / `crypto_algorithm_agility` / `crypto_verification_private` | M/S *(ap)* | N/A | Sin criptografía first-party | `SECURITY.md` |

### 4.6 ANALYSIS

| Criterio | Niv. | Estado | Acción | Archivo(s) |
|---|---|---|---|---|
| `static_analysis_common_vulnerabilities` | M | ✅ Met | bandit | — |
| `dynamic_analysis_unsafe` | M *(ap)* | N/A | Python memory-safe | — |

---

## 5. Sub-fases de ejecución

> Cada sub-fase = una PR independiente (rama `feat/...`), con DCO sign-off y CI verde.

### Sub-fase 2a — CI, cobertura y DCO  *(desbloquea el grueso de Quality)*
- **`.github/workflows/ci.yml`** (nuevo): jobs en push/PR →
  - `test`: instala deps y corre `pytest --cov` con **gate de cobertura ≥80%** sobre el código first-party.
  - `lint`: `ruff check` (warnings como error).
  - `sast`: `bandit -r`.
  - `dco`: valida `Signed-off-by` en los commits del PR.
- **Tests nuevos**: `deployment/eventPublisher/tests/test_event_publisher.py` (Flask test client + **mock de `confluent_kafka.Producer`** y del encoder) y `deployment/kafka_speed_exporter/tests/`. Requiere un **refactor menor** de `EventPublisher.py` a *app factory* / guardas a nivel módulo (igual que el `if __name__ == "__main__"` aplicado a `encoder_decoder.py`) para hacerlo importable y testeable.
- Config de cobertura/pytest para el árbol `eventPublisher` (en `pyproject.toml`/`pytest.ini` del servicio).
- Satisface: `automated_integration_testing`, `coding_standards_enforced`, `test_statement_coverage80`, `warnings_strict`, `dco` (enforcement), y de paso los SUGGESTED de Passing `test_continuous_integration` + `static_analysis_often`.

### Sub-fase 2b — Seguridad y aseguramiento
- **`docs/Threat-Model.md`** (nuevo): assurance case — activos, fronteras de confianza (API ↔ Kafka ↔ MQTT ↔ NiFi), amenazas (STRIDE breve) y mitigaciones. → `assurance_case`.
- **`EventPublisher.py`**: validación por **allowlist** de `sub_service`, formato/longitud de `geohash`, y límites de tamaño del payload; rechazo explícito de entradas inválidas. → `input_validation`, `implement_secure_design`.
- **`docs/Security-Architecture.md`** (nuevo): requisitos/expectativas de seguridad, postura TLS (brokers TLS 1.2+, verificación de certificados), agilidad de credenciales (env/`.env`), hardening. → `documentation_security`, `crypto_used_network`, `crypto_tls12`, `crypto_certificate_verification`, `crypto_credential_agility`, `hardening`.
- **`SECURITY.md`**: añadir **proceso de respuesta a vulnerabilidades** (triaje→fix→disclosure) y **crédito** a reporteros. → `vulnerability_response_process`, `vulnerability_report_credit`.
- Dockerfiles: fijar **digests** de imágenes base. → `build_repeatable`, `hardening`.

### Sub-fase 2c — Releases firmados
- Adoptar **Sigstore `gitsign`** para firmar los tags de versión; documentar el **proceso de verificación** (`gitsign verify` / `cosign`) en `RELEASE.md` y `docs/Development.md`. → `signed_releases`, `version_tags_signed`.
- Documentar **ruta de actualización** entre versiones SemVer. → `maintenance_or_update`.
- *(Acción humana)* los mantenedores firman los próximos tags.

### Sub-fase 2d — Gobernanza y documentación
- **`GOVERNANCE.md`** (nuevo): modelo de gobernanza, proceso de decisión, roles y responsabilidades, continuidad de acceso (≥2 admins). → `governance`, `roles_responsibilities`, `access_continuity`.
- **`ROADMAP.md`** (nuevo) + enlace en README: roadmap real a ≥1 año (reemplaza el placeholder). → `documentation_roadmap`.
- **`CONTRIBUTING.md`**: requisito DCO (`git commit -s`), guía de estilo concreta (**PEP 8** vía ruff), política de **tests de regresión**. → `dco`, `coding_standards`, `regression_tests_added50`.
- README: `alt` text en imágenes; revisar accesibilidad/i18n y justificar. → `accessibility_best_practices`, `internationalization`.

---

## 6. Acciones humanas / admin (no son código)

1. **Firmar los tags** de versión con gitsign (mantenedores) y, si se desea, habilitar la **GitHub App de DCO** (alternativa/complemento al check de CI).
2. **Branch protection** en `main`: exigir CI verde + 1 revisión (sienta base para Gold `two_person_review`).
3. **Rellenar el nivel Silver** en bestpractices.dev (criteria nivel 1) con la tabla §4 como guion.
4. Confirmar auto-declaraciones (`documentation_current`, `access_continuity`).

## 7. Archivos (resumen)

**Crear:** `docs/planes/openssf-fase2-silver.md` (este doc), `.github/workflows/ci.yml`, `GOVERNANCE.md`, `ROADMAP.md`, `docs/Threat-Model.md`, `docs/Security-Architecture.md`, `deployment/eventPublisher/tests/` (+ config pytest/cobertura), `deployment/kafka_speed_exporter/tests/`.

**Modificar:** `CONTRIBUTING.md`, `SECURITY.md`, `MAINTAINERS.md`, `README.md`, `RELEASE.md`, `CHANGELOG.md`, `docs/Development.md`, `deployment/eventPublisher/EventPublisher.py` (validación + factory), Dockerfiles (digests), `deployment/nifi/nifi-scripts/pyproject.toml` (si hace falta tocar config de cobertura/ruff).

## 8. Verificación (end-to-end)

1. **CI:** abrir una PR de prueba → los jobs `test`/`lint`/`sast`/`dco` pasan en GitHub Actions.
2. **Cobertura:** `pytest --cov` reporta **≥80%** statement coverage del código first-party (EventPublisher + exporter + nifi-scripts).
3. **DCO:** un commit sin `Signed-off-by` hace fallar el check; con `-s` pasa.
4. **Release firmado:** crear un tag de prueba firmado con gitsign y verificarlo (`gitsign verify` / cosign) según el doc.
5. **Threat model / seguridad:** `docs/Threat-Model.md` y `docs/Security-Architecture.md` existen y cubren fronteras de confianza, validación y TLS.
6. **Detección GitHub:** Insights → Community Standards sigue ✅; GOVERNANCE/ROADMAP presentes.
7. **Cobertura de criterios:** recorrer §4 y confirmar cada criterio Silver = Met / N/A justificado. Rellenar el formulario → **Silver**.

## 9. Riesgos / notas

- **Testabilidad de EventPublisher:** hoy ejecuta código a nivel de módulo (Flask app, `Producer`, `compile_files`). Para tests deterministas hay que refactorizar a *app factory* y **mockear Kafka**; riesgo bajo pero es un cambio de código real.
- **Cobertura 80%:** es el criterio Silver más costoso; concentra el esfuerzo de la Sub-fase 2a.
- **`build_repeatable`** bit-a-bit con Docker es difícil; fijar digests + deps es lo razonable y puede justificarse parcialmente.
- **Sigstore gitsign:** la firma de tags es keyless (OIDC); documentar bien la verificación para consumidores.
- Respetar convenciones del repo: cabeceras MIT en código nuevo; esquemas ASN.1 duplicados (no aplica aquí); `ruff.toml` raíz está bloqueado por hook → la config de ruff vive en `pyproject.toml`.
- El **Silver al 100%** lo cierra un mantenedor rellenando el formulario; el repo aporta la evidencia.
