# Plan — OpenSSF Best Practices Badge: Fase 1 «Passing (100%)»

> **Estado:** plan aprobado, **pendiente de implementación**. Este documento es el plan de seguimiento de la Fase 1. Las acciones aquí descritas aún **no se han ejecutado**.

---

## 1. Contexto

**InstantX** (LF Edge / Vodafone Business) está registrado en el OpenSSF Best Practices Badge Program como **proyecto 12224**, hoy en **0% / «In Progress»** (formulario prácticamente vacío) — verificado en `https://www.bestpractices.dev/en/projects/12224`.

El objetivo de **esta fase** es alcanzar el tramo **«Passing (100%)»** mejorando y reorganizando la documentación según las propias OpenSSF Best Practices, más un conjunto **mínimo** de artefactos de soporte técnico que algunos criterios `MUST` exigen y que no pueden afirmarse honestamente solo con prosa. Quedan **fuera de alcance** los criterios de Silver y Gold.

Hallazgos de la exploración que motivan el trabajo:
- La documentación de gobierno (`CONTRIBUTION`, `SECURITY`, `CODE_OF_CONDUCT`, `SUPPORT`, `MAINTAINERS`) vive bajo **`docs/`**, no en las ubicaciones estándar (raíz o `.github/`) que GitHub y la auto-detección de OpenSSF esperan. No existe `.github/`.
- **`docs/SUPPORT.md` está roto**: contiene una copia de la guía de contribución (137 líneas, titulada «Contributing to InstantX»), no contenido de soporte.
- El criterio `discussion` (MUST) no se cumple: el README cita un Google Group marcado **«NOT CREATED YET»**.
- No hay **linter** ni **análisis estático** (criterios `warnings` y `static_analysis`, MUST «si aplica»).
- La política de **tests** es implícita; falta declararla (`test_policy`, MUST).
- `docs/MAINTAINERS.md` referencia un `CONTRIBUTING.md` inexistente; `CONTRIBUTION.md` tiene una frase truncada (l.32: «report unacceptable behavior to.»).

## 2. Decisiones tomadas (preguntas bloqueantes — resueltas)

| # | Pregunta bloqueante | Decisión |
|---|---------------------|----------|
| 1 | `warnings` + `static_analysis` (MUST, difíciles de afirmar solo con docs) | **Tooling mínimo**: añadir `ruff` (lint) + `bandit` (SAST) sobre el código Python first-party y documentar su uso. **Sin CI.** |
| 2 | Mecanismo para `discussion` (MUST) | **Activar GitHub Discussions** en `lf-edge/instantx` y enlazarlo. (Requiere acción de admin del repo.) |
| 3 | Ubicación de los docs de gobierno | **Mover a la raíz** del repo y corregir todos los enlaces internos. |
| 4 | ¿Incluir mapeo del formulario + badge? | **Sí**: generar la tabla de justificación por criterio (este doc) y añadir el badge OpenSSF al README. |

## 3. Alcance

**Entra:** todos los criterios del nivel *Passing* (BASICS, CHANGE CONTROL, REPORTING, QUALITY, SECURITY, ANALYSIS); reorganización de docs a raíz; arreglo de `SUPPORT.md`; `ruff` + `bandit` + arreglo del test legacy; plantillas `.github/`; activación de Discussions; badge en README; doc de seguimiento `docs/planes/openssf-fase1-passing.md` con el mapeo de justificación.

**No entra:** criterios Silver/Gold; montar CI/CD (GitHub Actions) — `test_continuous_integration` y `static_analysis_often` quedarán como *unmet/SUGGESTED* (aceptable para Passing); reescritura funcional del código; nuevos tests de cobertura más allá de arreglar la suite existente.

---

## 4. Mapeo por criterio OpenSSF (núcleo del plan)

Leyenda nivel: **M** = MUST · **S** = SHOULD · **g** = SUGGESTED · *(ap)* = «si aplica».
«Respuesta» = lo que se marcará en el formulario de bestpractices.dev (proyecto 12224) con su evidencia.

### 4.1 BASICS

| Criterio | Niv. | Estado actual | Acción concreta | Archivo(s) | Respuesta + evidencia |
|---|---|---|---|---|---|
| `description_good` | M | README describe bien el proyecto (l.19-31) | Ninguna de fondo; usar como evidencia | `README.md` | **Met** → URL README |
| `interact` | M | README §Contributing/§Support remiten a las guías | Actualizar enlaces tras mover a raíz | `README.md` | **Met** → URL README |
| `contribution` | M | Guía existe pero en `docs/CONTRIBUTION.md` (GitHub no la detecta) | Mover/renombrar a `CONTRIBUTING.md` en raíz | `CONTRIBUTING.md` (nuevo), borrar `docs/CONTRIBUTION.md` | **Met** → URL CONTRIBUTING |
| `contribution_requirements` | S | §Verification cubre estilo/tests de forma suave | Añadir referencia explícita a política de tests y estándares de código | `CONTRIBUTING.md` | **Met** |
| `floss_license` | M | MIT + Apache-2.0 | Ninguna | `LICENSE.md` | **Met** |
| `floss_license_osi` | g | Ambas OSI-approved | Ninguna | `LICENSE.md` | **Met** |
| `license_location` | M | `LICENSE.md` en raíz | Opcional: renombrar a `LICENSE` para detección más robusta | `LICENSE.md` | **Met** |
| `documentation_basics` | M | README + `deployment/Quick-Start.md` + `docs/` | Enlazar build/uso desde README | `README.md`, `deployment/Quick-Start.md` | **Met** |
| `documentation_interface` | M | `docs/Event-Publisher-oas.yaml` (OpenAPI), `MQTT-Topic-Structure.md`, `Kafka.md`, `Encoding.md` | Ninguna; enlazar como evidencia | `docs/` (varios) | **Met** |
| `sites_https` | M | GitHub + GitHub Pages (`lf-edge.github.io/instantx`) en HTTPS | Ninguna | — | **Met** |
| `discussion` | M | **No cumple**: Google Group «NOT CREATED YET» | **Activar GitHub Discussions** (admin) + enlazar; quitar el «NOT CREATED YET» | `README.md`, `SUPPORT.md` + repo (admin) | **Met** → URL Discussions |
| `english` | S | Docs en inglés | Ninguna | — | **Met** |
| `maintained` | M | v2.0.0 (2025-03), commits recientes | Ninguna | — | **Met** |

### 4.2 CHANGE CONTROL

| Criterio | Niv. | Estado actual | Acción | Archivo(s) | Respuesta |
|---|---|---|---|---|---|
| `repo_public` | M | `github.com/lf-edge/instantx` público | Ninguna | — | **Met** |
| `repo_track` | M | Git | Ninguna | — | **Met** |
| `repo_interim` | M | Commits intermedios visibles | Ninguna | — | **Met** |
| `repo_distributed` | g | Git | Ninguna | — | **Met** |
| `version_unique` | M | SemVer (CHANGELOG 2.0.0/1.0.0) | Ninguna | `CHANGELOG.md` | **Met** |
| `version_semver` | g | SemVer 2.0.0 | Ninguna | `CHANGELOG.md` | **Met** |
| `version_tags` | g | Tags `v1.0.0`, `v2.0.0` | Ninguna | — | **Met** |
| `release_notes` | M | `RELEASE.md` + `CHANGELOG.md` | Corregir enlaces a docs movidos | `RELEASE.md`, `CHANGELOG.md` | **Met** |
| `release_notes_vulns` | M *(ap)* | No se mencionan vulnerabilidades | Añadir nota «Security fixes» (o «ninguna conocida») por release | `CHANGELOG.md`, `RELEASE.md` | **Met** |

### 4.3 REPORTING

| Criterio | Niv. | Estado actual | Acción | Archivo(s) | Respuesta |
|---|---|---|---|---|---|
| `report_process` | M | §«Reporting a bug» + GitHub Issues | Consolidar en `CONTRIBUTING.md` raíz | `CONTRIBUTING.md` | **Met** |
| `report_tracker` | S | GitHub Issues | Ninguna | — | **Met** |
| `report_responses` | M | Conductual (responder mayoría de reports 2-12 meses) | Declarar en formulario; verificar actividad de issues | — | **Met** (auto-declaración) |
| `enhancement_responses` | S | Conductual | Declarar/justificar en formulario | — | **Met/justificado** |
| `report_archive` | M | GitHub Issues = archivo buscable | Ninguna | — | **Met** |
| `vulnerability_report_process` | M | `docs/SECURITY.md` (no detectado por GitHub en `docs/`) | Mover a `SECURITY.md` raíz | `SECURITY.md` | **Met** → URL SECURITY |
| `vulnerability_report_private` | M *(ap)* | Email `instantxsupport@vodafone.com` | Ninguna | `SECURITY.md` | **Met** |
| `vulnerability_report_response` | M | No indica tiempo de respuesta | Añadir SLA: «respuesta inicial ≤ 14 días» | `SECURITY.md` | **Met** |

### 4.4 QUALITY

| Criterio | Niv. | Estado actual | Acción | Archivo(s) | Respuesta |
|---|---|---|---|---|---|
| `build` | M *(ap)* | docker-compose + Dockerfiles + Poetry | Documentar build reproducible en una sección dedicada | `README.md` o `docs/Development.md` | **Met** |
| `build_common_tools` | g | Docker, Poetry | Ninguna | — | **Met** |
| `build_floss_tools` | S | Toda la cadena es FLOSS | Ninguna | — | **Met** |
| `test` | M | `pytest` en `deployment/nifi/nifi-scripts` (6 tests) | Documentar la suite; **arreglar `DATA_FOLDER` hardcodeado** para que corra limpia | `deployment/nifi/nifi-scripts/tests/test_encoder_decoder.py`, `docs/Development.md` | **Met** |
| `test_invocation` | S | `poetry run pytest` | Documentar | `docs/Development.md`, `CONTRIBUTING.md` | **Met** |
| `test_most` | g | Cobertura parcial | Responder honestamente | — | **Met/unmet** |
| `test_continuous_integration` | g | Sin CI (decisión: sin CI esta fase) | Responder *unmet* (aceptable) | — | **Unmet** |
| `test_policy` | M | Implícita («include unit tests») | Declarar política: cambios funcionales mayores **DEBEN** incluir tests | `CONTRIBUTING.md` (+ `docs/Development.md`) | **Met** |
| `tests_are_added` | M | Existen tests para `encoder_decoder` | Reforzar política + recordatorio en plantilla de PR | `.github/PULL_REQUEST_TEMPLATE.md` | **Met** |
| `tests_documented_added` | g | No documentado en instrucciones de cambio | Recordatorio de tests en plantilla de PR | `.github/PULL_REQUEST_TEMPLATE.md` | **Met** |
| `warnings` | M *(ap)* | **Sin linter** | Añadir `ruff` sobre código first-party + documentar | `ruff.toml` (raíz), `docs/Development.md` | **Met** |
| `warnings_fixed` | M *(ap)* | — | Resolver/suprimir-justificado hallazgos de `ruff` | código Python first-party | **Met** |
| `warnings_strict` | g | — | Opcional (reglas estrictas) | `ruff.toml` | **Met/unmet** |

### 4.5 SECURITY

| Criterio | Niv. | Estado actual | Acción | Archivo(s) | Respuesta |
|---|---|---|---|---|---|
| `know_secure_design` | M | Mantenedores Vodafone | Auto-declaración (opcional: nota en `SECURITY.md`) | `SECURITY.md` | **Met** |
| `know_common_errors` | M | — | Auto-declaración | — | **Met** |
| `crypto_published`/`crypto_call`/`crypto_floss`/`crypto_keylength`/`crypto_working`/`crypto_weaknesses`/`crypto_pfs`/`crypto_password_storage`/`crypto_random` | M/S *(ap)* | El código first-party **no implementa criptografía** (UPER/ASN.1 ≠ cripto; TLS lo proveen los brokers configurables) | Marcar **N/A** con justificación; documentar postura | `SECURITY.md` (sección «Cryptography») | **N/A** (justificado) |
| `delivery_mitm` | M | Git sobre HTTPS/SSH (GitHub) | Ninguna | — | **Met** |
| `delivery_unsigned` | M | No se descargan hashes por HTTP sin verificar | Ninguna | — | **Met** |
| `vulnerabilities_fixed_60_days` | M | Sin vulns conocidas sin parchear | Auto-declaración | — | **Met** |
| `vulnerabilities_critical_fixed` | S | — | Auto-declaración | — | **Met** |
| `no_leaked_credentials` | M | `.gitignore` excluye `.env`/`passwords.properties`; `Quick-Start.md` lista credenciales **demo** | Verificar (grep) que no hay secretos reales + nota «credenciales por defecto, cambiar en producción» | `deployment/Quick-Start.md` | **Met** |

### 4.6 ANALYSIS

| Criterio | Niv. | Estado actual | Acción | Archivo(s) | Respuesta |
|---|---|---|---|---|---|
| `static_analysis` | M *(ap)* | **Ninguno** | Añadir `bandit` (SAST Python) sobre código first-party + documentar uso antes de release | `pyproject`/`.bandit`, `docs/Development.md` | **Met** |
| `static_analysis_common_vulnerabilities` | g | — | `bandit` cubre patrones comunes | — | **Met** |
| `static_analysis_fixed` | M *(ap)* | — | Resolver hallazgos medium+ | código Python first-party | **Met** |
| `static_analysis_often` | g | Sin CI | Responder *unmet* (aceptable) | — | **Unmet** |
| `dynamic_analysis` / `dynamic_analysis_unsafe` / `dynamic_analysis_enable_assertions` | g *(ap)* | No aplicado | Responder *unmet/N/A* (aceptable) | — | **Unmet/N/A** |
| `dynamic_analysis_fixed` | M *(ap)* | Sin análisis dinámico | **N/A** | — | **N/A** |

---

## 5. Cambios de documentación (reorganización a raíz)

> Patrón repetido: por cada archivo movido a la raíz, **corregir todos los enlaces relativos** que apuntaban a él o que él contenía (de `../X` a `./X` y viceversa) en README, RELEASE, CHANGELOG, AGENTS.md y entre los propios docs movidos.

1. **`CONTRIBUTING.md` (nuevo, raíz)** ← contenido consolidado de `docs/CONTRIBUTION.md`, corrigiendo: la frase truncada (l.32), enlaces relativos a raíz, y añadiendo la **política de tests** (`test_policy`) y referencia a estándares (`contribution_requirements`). **Borrar** `docs/CONTRIBUTION.md`.
2. **`SECURITY.md` (raíz)** ← `docs/SECURITY.md` + **SLA de respuesta ≤14 días** + sección **«Cryptography»** (postura N/A). **Borrar** `docs/SECURITY.md`.
3. **`CODE_OF_CONDUCT.md` (raíz)** ← `docs/CODE_OF_CONDUCT.md` (remite a LF Edge CoC). **Borrar** `docs/CODE_OF_CONDUCT.md`.
4. **`SUPPORT.md` (raíz) — REESCRIBIR**: el actual `docs/SUPPORT.md` está **roto** (duplica la guía de contribución). Crear contenido real de soporte: canales = **GitHub Discussions** (nuevo), Issues, Wiki, Stack Overflow. **Borrar** `docs/SUPPORT.md`.
5. **`MAINTAINERS.md` (raíz)** ← `docs/MAINTAINERS.md`, corrigiendo la referencia rota a `CONTRIBUTING.md`. **Borrar** `docs/MAINTAINERS.md`.
6. **`README.md`**: actualizar §Contributing/§Support/§Releases a las rutas de raíz; §Support con el enlace de Discussions y **sin** «NOT CREATED YET»; añadir **badge OpenSSF**; añadir sección breve de **Build & Test**.
7. **`RELEASE.md`** y **`CHANGELOG.md`**: corregir enlaces a docs movidos; añadir nota de `release_notes_vulns`.
8. **`AGENTS.md`** (y por tanto `CLAUDE.md`, symlink): actualizar la referencia `docs/CONTRIBUTION.md` → `CONTRIBUTING.md` (§7 Contribution Conventions).

**Badge para README** (criterio del entregable, Q4):
```markdown
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/12224/badge)](https://www.bestpractices.dev/projects/12224)
```

## 6. Artefactos de soporte mínimos (decisión Q1 — sin CI)

- **`ruff.toml` (raíz)**: configuración de lint cubriendo `deployment/eventPublisher/` y `deployment/nifi/nifi-scripts/`. Resolver/suprimir-justificado los hallazgos (`warnings`/`warnings_fixed`).
- **`bandit`**: config (`[tool.bandit]` en `deployment/nifi/nifi-scripts/pyproject.toml` y/o `.bandit` raíz) para `bandit -r deployment/eventPublisher deployment/nifi/nifi-scripts/src`. Resolver hallazgos medium+ (`static_analysis`/`static_analysis_fixed`).
- **`docs/Development.md` (nuevo)**: cómo construir (docker-compose/Poetry), correr tests (`poetry run pytest`), lint (`ruff check`) y SAST (`bandit`). Es la evidencia de `build`, `test`, `test_invocation`, `warnings`, `static_analysis`.
- **Arreglo del test legacy**: sustituir el `DATA_FOLDER` absoluto hardcodeado en `deployment/nifi/nifi-scripts/tests/test_encoder_decoder.py` por una ruta relativa al test, para que la suite corra limpia en cualquier máquina (`test` honesto).
- **`.github/PULL_REQUEST_TEMPLATE.md`**: checklist con recordatorio de tests (`tests_are_added`, `tests_documented_added`).
- **`.github/ISSUE_TEMPLATE/`**: plantillas `bug_report.md` y `feature_request.md` (refuerzan `report_process`).
- *(Opcional)* **`.github/CODEOWNERS`** desde `MAINTAINERS.md`.

> Dependencias de dev (`ruff`, `bandit`) se añaden al grupo dev de Poetry en `nifi-scripts` y se documentan para `eventPublisher` (vía `pipx`/venv) en `docs/Development.md`. No se modifica el runtime de producción.

## 7. Acciones que requieren un humano / admin (no son código)

Estas NO las puede ejecutar el agente; el plan las lista para que un mantenedor las complete:
1. **Activar GitHub Discussions** en `lf-edge/instantx` (Settings → Features). *(criterio `discussion`)*
2. **Rellenar el formulario** de bestpractices.dev (proyecto 12224) usando la tabla de §4 como guion de respuestas + URLs de evidencia. *(es lo que lleva el % al 100)*
3. Confirmar las **auto-declaraciones** de SECURITY (`know_secure_design`, `know_common_errors`, vulnerabilidades) y la actividad de respuesta a issues (`report_responses`).

## 8. Entregables y lista de archivos

**Crear:** `docs/planes/openssf-fase1-passing.md` (este doc), `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `MAINTAINERS.md` (raíz), `docs/Development.md`, `ruff.toml`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md` (opcional: `.github/CODEOWNERS`).

**Modificar:** `README.md`, `RELEASE.md`, `CHANGELOG.md`, `AGENTS.md`, `deployment/Quick-Start.md`, `deployment/nifi/nifi-scripts/pyproject.toml`, `deployment/nifi/nifi-scripts/tests/test_encoder_decoder.py`.

**Borrar:** `docs/CONTRIBUTION.md`, `docs/SECURITY.md`, `docs/CODE_OF_CONDUCT.md`, `docs/SUPPORT.md`, `docs/MAINTAINERS.md` (y `docs/LICENSE` duplicado, opcional).

## 9. Verificación (end-to-end)

1. **Enlaces:** ejecutar un comprobador de enlaces markdown (p. ej. `lychee` o `markdown-link-check`) sobre el repo; 0 enlaces rotos tras la reorganización.
2. **Detección GitHub:** confirmar que la pestaña *Insights → Community Standards* del repo marca ✅ README, CoC, Contributing, License, Security, Issue/PR templates.
3. **Tests:** `cd deployment/nifi/nifi-scripts && poetry install && poetry run pytest` pasa sin rutas hardcodeadas.
4. **Lint/SAST:** `ruff check .` y `bandit -r deployment/eventPublisher deployment/nifi/nifi-scripts/src` corren y no reportan errores medium+ sin resolver.
5. **Badge:** el markdown del badge renderiza en README apuntando a `projects/12224`.
6. **Cobertura de criterios:** recorrer la tabla de §4 y confirmar que cada criterio *Passing* tiene una respuesta aceptable (Met / N/A justificado / Unmet-pero-SUGGESTED). El % objetivo en bestpractices.dev tras rellenar el formulario = **100% Passing**.

## 10. Riesgos / notas

- El **100% real** solo se logra cuando un mantenedor rellena el formulario (paso §7.2); el repo aporta la evidencia, no el porcentaje.
- `report_responses`/`know_*` son **auto-declaraciones**: el plan asume que el equipo Vodafone puede afirmarlas con honestidad.
- Mover archivos a la raíz **rompe enlaces** temporalmente; la corrección de enlaces (§5) y la verificación (§9.1) son obligatorias antes del merge.
- Mantener la convención del repo: cabeceras de licencia MIT en código first-party nuevo; si se tocan esquemas ASN.1, actualizar **ambas** copias (no aplica en esta fase).
