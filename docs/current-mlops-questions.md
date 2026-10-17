# Current MLOps Workflow Discovery — Sanitized

## Purpose and confidentiality boundary

This document captures questions about the training-to-serving
workflow referenced in the assignment.

It contains no employer code, internal configurations, credentials,
customer records, model artifacts, internal resource identifiers,
or proprietary architecture diagrams.

AWS training, Azure serving, and Databricks data sharing are topics
to investigate, not verified descriptions of the implementation.

Unconfirmed details are marked "unknown / requires confirmation."

## 1. Known versus uncertain

| Area | Known from assignment context | Unknown / requires confirmation |
|---|---|---|
| AWS model training | AWS training is a discovery topic | Actual service, execution method, owner, and training trigger |
| Trained artifact | The assignment asks where it is stored and how it is versioned | Storage system, serialization format, registry, retention, and access controls |
| Azure model serving | Azure serving is a discovery topic | Actual serving service, runtime, model-loading mechanism, and deployment process |
| Artifact handoff | The assignment asks how the trained artifact reaches Azure | Transfer mechanism, deployment ownership, automation, integrity checks, and permissions |
| Databricks data sharing | Databricks sharing is a discovery topic | Sharing mechanism, producer, consumer, authorization, lineage, and schema-change process |

## 2. Questions about AWS training

1. What type of service or process executes training?
2. What triggers a training run: a person, schedule, pipeline, or event?
3. Which role or team owns the training workflow?
4. How are the training code revision and dependency environment recorded?
5. How is the training dataset or snapshot identified?
6. What evaluation checks are required before a model can be promoted?

## 3. Questions about artifact storage and versioning

1. What type of storage or registry holds the trained artifact?
2. What is the artifact format?
3. Are preprocessing objects packaged with the estimator?
4. Does each training run produce an immutable artifact version?
5. Can a deployed version be traced to its training run and code revision?
6. Is a checksum or other integrity check used?
7. Who is permitted to publish, approve, or read artifacts?

## 4. Questions about the handoff to Azure serving

1. Does deployment push the artifact to Azure, or does serving pull it?
2. What type of pipeline or process performs the handoff?
3. Is promotion automatic, approval-based, or manual?
4. How are training and serving dependencies kept compatible?
5. Is the artifact loaded at startup or through another mechanism?
6. How is the active model version exposed or recorded?
7. How is a previous version restored after a failed deployment?
8. What monitoring detects loading failures or prediction errors?

## 5. Questions about Databricks data sharing

1. What approved mechanism makes data available to consumers?
2. Are consumers accessing shared tables, exported files, or another interface?
3. What role does the shared data play: training, batch scoring,
   online features, reporting, or something else?
4. How are permissions granted and reviewed?
5. How are schema changes communicated?
6. How are dataset versions, freshness, and lineage tracked?
7. Who owns the producer-consumer contract?

## 6. Investigation method

- Ask an authorized engineer for a generic workflow explanation.
- Review documentation only where access and use are permitted.
- Do not copy internal files, screenshots, diagrams, or identifiers.
- Record only findings that are safe for a public learning repository.
- Keep confidential findings outside this repository.
- Leave unverified answers explicitly marked as unknown.

## 7. Findings log

| Topic | Sanitized finding | Status | Evidence |
|---|---|---|---|
| AWS training execution | Unknown / requires confirmation | Open | Not yet confirmed |
| Artifact storage | Unknown / requires confirmation | Open | Not yet confirmed |
| Artifact versioning | Unknown / requires confirmation | Open | Not yet confirmed |
| Artifact transfer to Azure | Unknown / requires confirmation | Open | Not yet confirmed |
| Azure serving runtime | Unknown / requires confirmation | Open | Not yet confirmed |
| Deployment and rollback | Unknown / requires confirmation | Open | Not yet confirmed |
| Databricks sharing mechanism | Unknown / requires confirmation | Open | Not yet confirmed |

## 8. What the local project demonstrates

The synthetic project demonstrates a workflow I implemented directly:

- Generate synthetic tabular data locally.
- Fit a preprocessing-and-classification Pipeline.
- Save the fitted Pipeline and metadata as artifacts/model.joblib.
- Load the trusted artifact through ModelService.
- Serve predictions through FastAPI.
- Return the model version with predictions.
- Validate behavior with automated tests.

These local implementation choices are not claims about the
organization's AWS, Azure, or Databricks architecture.

## 9. Current conclusion

The local model lifecycle has been implemented and tested.
The organizational workflow remains unconfirmed.

The next discovery priority is to establish, where permitted:
1. Where the trained artifact is stored.
2. How its version is identified.
3. How that version reaches the Azure serving environment.
