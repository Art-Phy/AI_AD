This project follows Semantic Versioning (SemVer-style while experimental).

---

### Unreleased

---

### v1.1.0 - 25.10.2026

#### Added

- Added the first functional Machine Learning baseline.
- Added a pilot dataset with 60 balanced samples:
  - 30 human-written texts.
  - 30 AI-generated texts.
  - 10 topics with 6 samples per topic.
- Added the `DatasetSample` data model for ML samples.
- Added a CSV dataset loader with validation for structure, labels, text length, and duplicate IDs.
- Added ML-specific feature extraction.
- Added ordered feature vectors for model training.
- Added stratified train/test splitting.
- Added a training pipeline based on:
  - `StandardScaler`
  - `LogisticRegression`
- Added evaluation metrics:
  - accuracy
  - precision
  - recall
  - F1
  - confusion matrix
- Added stratified cross-validation using `StratifiedKFold`.
- Added sample-level error analysis.
- Added tests for dataset handling, loading, feature extraction, training, evaluation, and cross-validation.

#### Changed

- Replaced direct `LogisticRegression` training with a scikit-learn `Pipeline` including feature standardization.
- Replaced the previous tuple-based dataset interface with `DatasetSample`.
- Normalized ML predictions to native Python integers to avoid exposing NumPy-specific types.
- Updated project documentation to describe the experimental ML baseline and its current limitations.

#### Experimental

- The ML baseline currently uses five features:
  - `avg_sentence_length`
  - `sentence_length_variance`
  - `lexical_diversity`
  - `punctuation_ratio`
  - `max_word_frequency_ratio`
- Cross-validation on the pilot dataset achieved a mean accuracy of `0.917`.
- Mean precision was `0.891`.
- Mean recall was `1.000`.
- Mean F1 score was `0.935`.
- Error analysis identified 5 false positives, all corresponding to human-written texts classified as AI.
- Three of the five false positives belonged to the `social_media` topic.
- The current dataset contains samples from a single human author and a single AI generator.
- The current results should be considered experimental and are not representative of production performance.
- The ML system is not yet integrated into the CLI, API, or Web UI.
- The public detector continues to use the stable heuristic system.

---

### v1.0.2 - 22.07.2026

#### Added

- Added a new Deployment section to the README.
- Documented environment variables for deployment.
- Improved formatting and examples throughout the documentation.

#### Deployment

- Validated full deployment on Linux using `systemd`.
- Added configuration through `EnvironmentFile`.
- Verified correct operation after system restart.
- Validated persistent deployment on Raspberry Pi.

---

### v1.0.1 - 12.07.2026

#### Added

- Added API host configuration through `AIDETECT_API_HOST`.
- Added API port configuration through `AIDETECT_API_PORT`.

#### Deployment

- Prepared the `aidetect-api` command for deployment on servers and local networks.

---

### v1.0.0 - 06.06.2026

#### Stable Release

- First stable release of the project.
- Consolidated all functionality developed throughout the v0.x series.
- Prepared for use as a CLI tool, REST API, and integrated Web UI.

#### Packaging

- Distributed as an installable Python package.
- Added new commands:
  - `aidetect-cli`
  - `aidetect-api`
- Added configuration through `pyproject.toml`.

#### Infrastructure

- Completed a full review of the project structure and configuration.
- Validated installation in a clean environment.
- Updated documentation and stable version metadata.

#### Testing

- Validated the complete test suite before release.
- Verified compatibility across CLI, API, UI, reporting, logging, and security.

---

### v0.9.0 - 09.03.2026

#### Added

- Added the `include_text` option to the `/v1/analyze/text/report` endpoint.
- Allows the full text to be included in the report only when explicitly requested.

#### Privacy

- Reports store only `text_length` by default.
- Full text is stored only when `include_text=true`.

#### UI

- Added a Web UI checkbox to include the full text in the report.
- Added a privacy notice to help prevent accidental storage of sensitive content.

---

### v0.8.0 - 05.03.2026

#### Added

- Added structured JSON logging with one line per event for traceability and observability.
- Added environment-based configuration for log level and rotating log files.

#### Environment

- `AIDETECT_LOG_LEVEL` (default: `INFO`)
- `AIDETECT_LOG_FILE` (optional): log file path. If undefined, logs are written only to console.
- `AIDETECT_LOG_MAX_BYTES` (default: `1000000`)
- `AIDETECT_LOG_BACKUP_COUNT` (default: `3`)

---

### v0.7.0 - 27.02.2026

#### Added

- Added the `POST /v1/analyze/text/report` endpoint returning a complete report with metadata.
- Added optional report persistence through `AIDETECT_REPORTS_DIR`.
- Updated the Web UI to consume the report endpoint and download the report exactly as returned by the API.

#### Environment

- `AIDETECT_REPORTS_DIR` (optional): directory where JSON reports are stored.

---

### v0.6.0 - 18.02.2026

#### Added

- Added `GET /version` to expose the running service version.
- Added `request_id` middleware:
  - Generates `X-Request-ID` for each response or preserves the client-provided value.
- Added basic per-request logging including method, path, status, duration, and request ID.
- Added JSON report export from the Web UI.

---

### v0.5.0 - 10.02.2026

#### Added

- Added an integrated FastAPI Web UI (`GET /ui`) for non-technical users.
- Added static asset serving through `/static/app.js`.
- Improved UX with result summaries and a button to copy generated JSON.

#### Notes

- The API remains protected by API key authentication and rate limiting.
- The UI acts as a lightweight layer over `/v1/analyze/text`.

---

### v0.4.2 - 02.02.2026

#### Fixed

- API keys passed through the query parameter (`?api_key=...`) are accepted only when `AIDETECT_UI_MODE=1`.
- In normal mode (`AIDETECT_UI_MODE=0`), authentication is performed exclusively through the `X-API-Key` header.

---

### v0.4.1 - 31.01.2026

#### Added

- Added a UI-friendly authentication mode for local use.
- Added support for passing the API key through the query parameter (`?api_key=...`) **only** when `AIDETECT_UI_MODE=1`.

#### Changed

- UI mode detection is now evaluated at runtime to simplify testing and dynamic configuration.

#### Security

- API key authentication through query parameters is **disabled by default**.
- `/v1/*` endpoints continue to require an API key unless explicit local UI mode is enabled.

---

### v0.4.0 - 25.01.2026

#### Added

- Added API key authentication for `/v1/*` endpoints.
- Added a public health check at `/health`.
- Added in-memory rate limiting per API key.
- Added tests for authentication and rate limiting responses (`401` and `429`).

#### Changed

- Rate limiting configuration is now read from environment variables for easier testing and deployment.

#### Fixed

- Corrected environment variable names for API keys.

---

### v0.3.0 - 18.01.2026

#### Added

- Added a REST API using FastAPI for text analysis.
- Added automatic Swagger documentation at `/docs`.
- Added `/v1/analyze/text` with mode support.
- Added `/v1/modes` to expose available detection modes.
- Added `/health` for health checks.
- Added API tests using Starlette `TestClient` and `httpx`.

#### Changed

- Expanded the README with a dedicated API section.

---

### v0.2.0 - 31.12.2025

#### Added

- Added configurable detection modes: `conservative`, `balanced`, and `aggressive`.
- Added clear separation between scoring and classification policy.
- Added the active mode to result output.

#### Changed

- Decoupled score interpretation from metric calculation.
- Extended the CLI with the `--mode` option.

#### Fixed

- Fixed configuration flow from CLI to the detector core.

---

### v0.1.0 - 26.12.2025

#### Added

- Added a heuristic-based text authorship detector.
- Added a functional CLI with output options.
- Added explainable linguistic metrics.
- Added decoupled threshold configuration.

#### Changed

- Introduced a modular architecture for text analysis.

#### Fixed

- Fixed imports and package execution configuration.

---

### v0.0.0 - 17.12.2025

- Added the initial project structure.
- Added README, LICENSE, CHANGELOG, requirements, and base configuration.
- Added the base `aidetect` package and test directory.
